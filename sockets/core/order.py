from tortoise import Tortoise 
from django.conf import settings
from ..tortoise_models import Order
from .utils import parse_event

class OrderProcessing:

    def __init__(self,*args, **kwargs):
        super().__init__(**kwargs)

    async def order_service(self,*args, **kwargs):
        await Tortoise.init(config=settings.TORTOISE_INIT)
        await Tortoise.generate_schemas()
        pars_data = await parse_event(**kwargs)
        pars_data['type'] = kwargs['type']
        order = await Order.filter(order_id=pars_data['order_id'])
        if len(order) > 0:
            for update_order in order:
                obj = await update_order.update_or_create(**pars_data)
        else:
            data = await Order.get_or_create(**pars_data)
        await Tortoise.close_connections()


