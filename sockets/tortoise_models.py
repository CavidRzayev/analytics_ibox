from tortoise import fields
from tortoise.models import Model
from tortoise.signals import post_delete, post_save, pre_delete, pre_save
from channels.layers import get_channel_layer
from asgiref.sync import sync_to_async
from asgiref.sync import async_to_sync


class DefaultModel(Model):
    type = fields.CharField(max_length=50, null=True)
    status = fields.CharField(max_length=50, null=True)
    status_message = fields.CharField(max_length=150, null=True)
    created = fields.DatetimeField(auto_now_add=True)
    modified = fields.DatetimeField(auto_now=True)
    description = fields.TextField(null=True)
    shop_id = fields.IntField(null=True)

    def __str__(self):
        return self.type

  
    

class Order(DefaultModel):
    order_id = fields.IntField(null=True)
    payment_id = fields.IntField(null=True)
    user_id = fields.IntField(null=True)
    merchant_id = fields.IntField(null=True)
    courier_id = fields.IntField(null=True)
    point = fields.IntField(null=True)

    class Meta:
        table = 'socket_order'
        indexes=("order_id","payment_id",)

    def __str__(self):
        return str(self.id)


class Payment(DefaultModel):
    order = fields.ForeignKeyField('models.Order', related_name='order_payments')

    class Meta:
        table = 'socket_payment'
    

@pre_save(Payment)
async def signal_pre_save(sender, instance: Payment, using_db, update_fields) -> None:
    channel_layer = get_channel_layer()
    if instance.status == 'Paid':
        order = await Order.update_or_create(status = "Success",
        status_message=instance.status_message,
        description=instance.description,
        type=instance.type,
        order_id=instance.order_id,
        payment_id=instance.id)
        
        await channel_layer.group_send(
            "managers",
            {'type': 'userflow.payment',
            'data': instance.order_id,
            })