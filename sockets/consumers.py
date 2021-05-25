from channels.generic.websocket import AsyncWebsocketConsumer,AsyncJsonWebsocketConsumer,WebsocketConsumer,StopConsumer
import json
from django.contrib.auth.models import User
from channels.db import database_sync_to_async
from .core.order import OrderProcessing
from .core.payment import PaymentProcessing
from .core.logging import LoggingProcessing
from .core.integration import IntegrationProcessing
from django.core.serializers.json import DjangoJSONEncoder
from datetime import date, datetime

from channels.exceptions import StopConsumer


class AnalyticsConsumers(AsyncJsonWebsocketConsumer):
    
    payment = PaymentProcessing()
    order = OrderProcessing()
    logging = LoggingProcessing()
    integration = IntegrationProcessing()

    async def json_serial(self,obj):

        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        raise TypeError ("Type %s not serializable" % type(obj))


    #async def websocket_disconnect(self, event):
    # Leave room group
        #await self.channel_layer.group_discard(
            #self.room_name,
         #   self.channel_name
        #)
        #raise StopConsumer()

    async def connect(self):
#        self.group_name = "main"
        #await self.channel_layer.group_add(
          #      self.group_name,
         #       self.channel_name)
        await self.accept()
    
    async def echo_message(self, event):
        
        await self.send_json(event)
    
    async def disconnect(self,code):
 #       await self.channel_layer.group_discard(self.group_name, self.channel_name)
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

    async def order_type_check_data(self,*args, **kwargs):
        send = await self.order.order_service(**kwargs)
        if send[1] == True:
            new_data = await send[0].get_or_none(id=send[0].id).values('order_id','id','user_id','type','status','payment_status','payment_id','description','merchant_id','point','courier_id')
            try:
                await self.channel_layer.group_send(
                         'orders',
                       {
                        'type': 'create.echo.message',
                        'message': new_data
                       }
                        )
            except:
                pass

    async def logging_type_check_data(self, payment=False,*args, **kwargs):
        start_processing = await self.logging.logging_service(**kwargs)
#        time = json.dumps(start_processing.timestamp, indent=4, sort_keys=True, default=str)
        new_log =  await start_processing.get(id=start_processing.id).values("id","type","message","content","status")
        try:
            await self.channel_layer.group_send(
                    'managers',
                    {
                        'type': 'logging.echo.message',
                        'message': new_log,
                        'timestamp': json.dumps(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                        'payment_status':payment
                    }
                )
        except:
            pass
        
    
    async def integration_type_check_data(self, payment=False,*args, **kwargs):
        start_processing = await self.integration.integration_service(**data)
 #       time = json.dumps(start_processing.timestamp, indent=4, sort_keys=True, default=str)
        new_log =  await start_processing.get(id=start_processing.id).values("id","type","message","content","status")
        await self.channel_layer.group_send(
                    'managers',
                    {
                        'type': 'integration.echo.message',
                        'message': new_log,
                        'timestamp': json.dumps(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                    }
                )
        



    async def parse_data(self,data):
        print(data)
        data_type = data['type'].split('_')
        if "checkout" == data_type[1]:
            await self.order_type_check_data(**data)
        elif "draft" == data_type[1]:
#            print(data)
            await self.order_type_check_data(**data)
        
        # elif "payment" in data_type[1]:
        #     await self.payment.payment_services(**data)
        elif "logging" in data_type[1]:
            await self.logging_type_check_data(**data)
        elif "payment" in data_type[1]:
            data['payment'] = True
            await self.logging_type_check_data(**data)
        elif "integration" in data_type[1]:
            await self.integration_type_check_data(**data)
        await self.echo_message(data)
       
    
