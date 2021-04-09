from tortoise import Tortoise 
from django.conf import settings
from ..tortoise_models import Payment
from .utils import parse_event,get_order

class PaymentProcessing():
    def __init__(self,*args, **kwargs):
        super().__init__(**kwargs)

    async def get_payment_update(self,payment_id,**kwargs):
        data = await parse_event(**kwargs)
        payment = await Payment.get(id=payment_id)
        payment.type = kwargs['type']
        payment.status = data.get('status',None)
        payment.status_message = data.get('status_message',None)
        payment.description = data.get('description',None)
        await payment.save()
        return payment
    

    async def payment_get_or_create(self,order_id):
        payment, query_status = await Payment.get_or_create(order_id=order_id)
        return payment

    
    async def payment_services(self,**kwargs):
        await Tortoise.init(config = settings.TORTOISE_INIT)
        await Tortoise.generate_schemas()
        pars_data = await parse_event(**kwargs)
        order = await get_order(pars_data['order_id'])
        if order is not None:
            payment =  await self.payment_get_or_create(order.id)
            payment_update = await self.get_payment_update(payment.id,**kwargs)
        await Tortoise.close_connections()

