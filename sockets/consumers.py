from channels.generic.websocket import AsyncWebsocketConsumer,AsyncJsonWebsocketConsumer,WebsocketConsumer,StopConsumer
import json
from django.contrib.auth.models import User
from channels.db import database_sync_to_async
from .services import order_service,payment_services

class AnalyticsConsumers(AsyncJsonWebsocketConsumer):
    
    async def connect(self):
        await self.accept()
    
    async def echo_message(self, event):
        await self.send_json(event)
    
    async def disconnect(self,code):
        raise StopConsumer()

    async def receive_json(self, content):
        convert_dumps = json.dumps(content)
        message = json.loads(convert_dumps)
        if self.scope['auth'] == True:
             await self.parse_data(message)
        else:
            await self.parse_data({
                'error': "Authorization error"
            })
    
    async def parse_data(self,data):
        data_type = data['type'].split('_')
        if "order" in data_type[0]:
            await order_service(**data)
        if "payment" in data_type[1]:
            await payment_services(**data)            
        await self.echo_message(data)
       
    async def order_view(self, event):
        type = event['type']
        order_id = event['data'][0]['order_id']
        status = event['data'][0]['status']
        await self.send_json({
            'type': type,
            'order_id': username,
            'status': status,
        })
    

        