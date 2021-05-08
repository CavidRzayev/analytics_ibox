from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json
from django.contrib.auth.models import User
from channels.db import database_sync_to_async
from tortoise import Tortoise
from django.conf import settings
from ...tortoise_models import Order
from asgiref.sync import sync_to_async

from django.core.serializers.json import DjangoJSONEncoder


async def get_order(data):
    Tortoise.init(config = settings.TORTOISE_INIT)
    order = await Order.filter(order_id=data['event'])
    await Tortoise.close_connections()


class UserFlowConsumers(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    async def connect(self):
        # if self.scope['user'].is_manager:
        self.group_name = "managers"
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name)
        await self.accept()

    async def create_echo_message(self, event):
        await self.send_json(event)


    async def receive_json(self, content):
        convert_dumps = json.dumps(content)
        message = json.loads(convert_dumps)
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'userflow_data',
                'message': message
            }
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)



    async def userflow_payment(self,event):
        await Tortoise.init(**settings.TORTOISE_INIT)
        order = await Order.filter(order_id=event['data']).exclude(payment_id=None).order_by("-id").first().values()
        
        a = json.dumps(order,
        sort_keys=True,
        indent=1,
        cls=DjangoJSONEncoder)
       
        
        await self.send_json(json.loads(a))
        
   

    
    
    