from tortoise import fields
from tortoise.models import Model
from .defaultmodel import DefaultModel
from tortoise.signals import post_delete, post_save, pre_delete, pre_save
from .ordermodel import Order


class Payment(DefaultModel):
    order = fields.ForeignKeyField('models.Order', related_name='order_payments')

    class Meta:
        table = 'socket_payment'
    

@pre_save(Payment)
async def signal_pre_save(sender, instance: Payment, using_db, update_fields) -> None:
    if instance.status == 'Paid':
        order = await Order.update_or_create(status = "Success",
        status_message=instance.status_message,
        description=instance.description,
        type=instance.type,
        order_id=instance.order_id,
        payment_id=instance.id)