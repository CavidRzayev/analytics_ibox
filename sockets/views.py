from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from asgiref.sync import sync_to_async
from tortoise import Tortoise
from django.conf import settings
from .tortoise_models import Order,Payment

def index(request):
    return render(request, 'index.html')


async def order(request, order_id):

    await Tortoise.init(**settings.TORTOISE_INIT)
    order = await Order.all().values()
    await Tortoise.close_connections()
    return await sync_to_async(JsonResponse)(order, safe=False)