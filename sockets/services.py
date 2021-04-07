from tortoise import Tortoise 
from django.conf import settings
from .tortoise_models import Order,Payment


async def get_payment_update(payment_id,**kwargs):
    data = await parse_event(**kwargs)
    payment = await Payment.get(id=payment_id)
    payment.type = kwargs['type']
    payment.status = data.get('status',None)
    payment.status_message = data.get('status_message',None)
    payment.description = data.get('description',None)
    await payment.save()
    return payment
    

async def payment_get_or_create(order_id):
    payment, query_status = await Payment.get_or_create(order_id=order_id)
    return payment

async def get_order(order_id):
    order = await Order.get_or_none(order_id=order_id)
    return order

async def parse_event(**kwargs):
    data = [x for x in kwargs['data']]
    return data[0]

async def order_service(**kwargs):
    await Tortoise.init(**settings.TORTOISE_INIT)
    await Tortoise.generate_schemas()
    pars_data = await parse_event(**kwargs)
    order = await Order.filter(order_id=pars_data['order_id'])
    if len(pars_data) > 0:
        for update_order in order:
            obj = update_order.update_from_dict(data=kwargs)
            await obj.save()
    else:
        data = await Order.create(**kwargs)
    await Tortoise.close_connections()


async def payment_services(**kwargs):
    await Tortoise.init(**settings.TORTOISE_INIT)
    await Tortoise.generate_schemas()
    pars_data = await parse_event(**kwargs)
    order = await get_order(pars_data['order_id'])
    if order is not None:
        payment =  await payment_get_or_create(order.id)
        payment_update = await get_payment_update(payment.id,**kwargs)
    await Tortoise.close_connections()
    