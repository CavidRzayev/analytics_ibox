from tortoise import Tortoise 
from django.conf import settings
from ..tortoise_models import Order
from .utils import parse_event
from channels.db import database_sync_to_async

class OrderProcessing:

    def __init__(self,*args, **kwargs):
        super().__init__(**kwargs)

    async def check_order(self,*args, **kwargs):
        return await Order.filter(type=kwargs['type']).filter(order_id=kwargs['order_id']).filter(is_active=True)

    async def update_status_order(self,*args, **kwargs):
        return await Order.filter(order_id=kwargs['order_id']).filter(is_active=True).update(is_active=False)

    async def order_service(self,*args, **kwargs):
        await Tortoise.init(settings.TORTOISE_INIT)
        await Tortoise.generate_schemas()
        pars_data = await parse_event(**kwargs)
        pars_data['type'] = kwargs['type']
        check = await self.check_order(**pars_data)
        print(check)
        if len(check) > 0:
           return check, False
        else:
            await self.update_status_order(**pars_data)
            data = await Order.get_or_create(**pars_data)
            return data
        await Tortoise.close_connections()


