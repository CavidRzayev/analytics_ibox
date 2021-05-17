#from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from asgiref.sync import sync_to_async
from tortoise import Tortoise
from django.conf import settings
from .tortoise_models import Order,Payment, Logging
from tortoise.query_utils import Q
from django.core.paginator import Paginator
from rest_framework.authtoken.models import Token
from user.models import User
from channels.db import database_sync_to_async


def logins(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            create_token = Token.objects.get_or_create(user=user)
            return HttpResponseRedirect('order')
        else:
            return HttpResponseRedirect('login')
    if request.user.is_authenticated:
        return HttpResponseRedirect('order')
    return render(request,'login.html')

@database_sync_to_async
def get_user(*args,**kwargs):
    try:
        user = User.objects.get(id=args[0].user.id)
        if  user.is_authenticated:
            return True,user.auth_token
        else:
            return False, None
    except:
        return False, None
    


async def order(request):
    await Tortoise.init(settings.TORTOISE_INIT)
    user =  await get_user(request)
    if  user[0] == True:
       all_orders = await Order.all().group_by('id','created','type').exclude(is_active=False).order_by('-id').values('order_id','user_id','type','status','point','payment_status','merchant_id','payment_id','created','is_active')
       context = {
            "order":all_orders,
            "token":user[1],
        }
       await Tortoise.close_connections()
       return render (request,'order.html',context)
    else:
        return HttpResponseRedirect('login')


async def logging(request):
    await Tortoise.init(settings.TORTOISE_INIT)
    user =  await get_user(request)
    if  user[0] == True:
        all_loggings = await Logging.all().order_by('-id').values("id",'content','message','status','type','timestamp')
        q = request.GET.get('q')
        if q:
            all_loggings = await Logging.filter(content__icontains=q).order_by('-id').values("id",'content','message','status','type','timestamp')
        paginator = Paginator(all_loggings, 500)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        await Tortoise.close_connections()
        return render(request,'logging.html',{'obj':page_obj,"token":user[1]})
    else:
       return HttpResponseRedirect('login')


async def order_detail(request,order_id):
    await Tortoise.init(settings.TORTOISE_INIT)
    user =  await get_user(request)
    if  user[0] == True:
        order = await Order.filter(order_id=order_id).first()
        order_draft = await Order.get_or_none(order_id=order_id).filter(type='order_draft').distinct()
        order_checkout = await Order.get_or_none(order_id=order_id).filter(type='order_checkout').distinct()
        order_payment = await Order.get_or_none(order_id=order_id).filter(type='order_payment').distinct()
        order_processing = await Order.get_or_none(order_id=order_id).filter(type='processing').distinct()
        context = {
            'order':order,
            'order_draft':order_draft,
            'order_checkout':order_checkout,
            'order_payment':order_payment,
            'order_processing':order_processing
        }
        await Tortoise.close_connections()
        return render (request,'order_detail.html',context)
    else:
        return HttpResponseRedirect('login')

async def logging_payment(request):
    await Tortoise.init(settings.TORTOISE_INIT)
    user =  await get_user(request)
    if  user[0] == True:
        logging_payment = await Logging.filter(type="realtime_payment").order_by('-id').values("id",'content','message','status','type','timestamp')
        q = request.GET.get('q')
        if q:
            logging_payment = await Logging.filter(type="realtime_payment").filter(content__icontains=q).order_by('-id').values("id",'content','message','status','type','timestamp')
        paginator = Paginator(logging_payment, 100)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        await Tortoise.close_connections()
        return render(request,'logging_payment.html',{'obj':page_obj,"token":user[1]})
    else:
        return HttpResponseRedirect('login')

