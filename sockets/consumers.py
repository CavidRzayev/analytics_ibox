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
        
        if "checkout" or 'draft' in data_type[1]:
            send = await self.order.order_service(**data)
            if send[1] == True:
                new_data = await send[0].get_or_none(id=send[0].id).values('order_id','id','user_id','type','status','payment_status','payment_id','description','merchant_id','point')
                await self.channel_layer.group_send(
                    'managers',
                    {
                        'type': 'new.create.echo.message',
                        'message': new_data
                    }
                )
        if "payment" in data_type[1]:
            await self.payment.payment_services(**data)            
        await self.echo_message(data)
       
    
    

        