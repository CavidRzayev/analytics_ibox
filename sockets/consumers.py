from channels.generic.websocket import AsyncWebsocketConsumer,AsyncJsonWebsocketConsumer,WebsocketConsumer,StopConsumer
import json
from django.contrib.auth.models import User
from channels.db import database_sync_to_async
from .core.order import OrderProcessing
from .core.payment import PaymentProcessing

class AnalyticsConsumers(AsyncJsonWebsocketConsumer):
    
    payment = PaymentProcessing()
    order = OrderProcessing()

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
        print(data)
        if "checkout" or "draft" in data_type[1]:
            await self.order.order_service(**data)
       
        if "payment" in data_type[1]:
            await self.payment.payment_services(**data)            
        await self.echo_message(data)
       
    
    

        