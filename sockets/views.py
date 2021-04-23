from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from asgiref.sync import sync_to_async
from tortoise import Tortoise
from django.conf import settings
from .tortoise_models import Order,Payment
from tortoise.query_utils import Q


async def order(request):
    # await Tortoise.init(**settings.)
    await Tortoise.init(**settings.TORTOISE_INIT)
    order = await Order.all()
    await Tortoise.close_connections()
    return render (request,'order.html',{'order':order})