
from ..tortoise_models import Order,Payment


async def get_order(order_id):
    order = await Order.get_or_none(order_id=order_id,type='order_checkout')
    return order

async def parse_event(**kwargs):
    data = [x for x in kwargs['data']]
    return data[0]