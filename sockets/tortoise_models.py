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
    point = fields.IntField(null=True,default=1)
    payment_status = fields.IntField(null=True)
    payment_method = fields.IntField(null=True)
    is_active = fields.BooleanField(default=True)

    class Meta:
        table = 'socket_order'
        indexes=("order_id","payment_id",)

    def __str__(self):
        return str(self.id)

    async def save(self,force_create,*args, **kwargs):
        # if force_create is True:
        if self.type == 'order_draft':
             self.point = 1
        elif self.type == "order_checkout":
            self.point = 2
        elif self.type == "order_payment":
            self.point = 3
        elif self.type == "order_processing":
            self.point = 4
        elif self.type == "order_done":
            self.point = 5
        await super().save(*args, **kwargs)
        
class Payment(DefaultModel):
    order = fields.ForeignKeyField('models.Order', related_name='order_payments')

    class Meta:
        table = 'socket_payment'
    


class Logging(Model):
    type = fields.CharField(max_length=50, null=True)
    message = fields.CharField(max_length=1000, null=True)
    content = fields.TextField(null=True)
    status = fields.CharField(max_length=100, null=True)
    timestamp = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "socket_logging"





# @pre_save(Payment)
# async def signal_pre_save(sender, instance: Payment, using_db, update_fields) -> None:
#     channel_layer = get_channel_layer()
#     if instance.status == 'Paid':
#         get_order = await Order.get(id=instance.order_id)
#         print(get_order.id)
#         order = await Order.update_or_create(status = "success",
#         status_message=instance.status_message,
#         description=instance.description,
#         type=instance.type,
#         order_id=get_order.order_id,
#         payment_id=instance.id,
#         point=2)
#         print('data', instance.order_id)
#         await channel_layer.group_send(
#             "managers",
#             {'type': 'userflow.payment',
#             'data': get_order.order_id,
#             })