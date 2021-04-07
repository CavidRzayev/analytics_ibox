from tortoise import fields
from tortoise.models import Model

class DefaultModel(Model):
    type = fields.CharField(max_length=50, null=True)
    status = fields.CharField(max_length=50, null=True)
    status_message = fields.CharField(max_length=150, null=True)
    created = fields.DatetimeField(auto_now_add=True)
    modified = fields.DatetimeField(auto_now=True)
    description = fields.TextField(null=True)

class Order(DefaultModel):
    id = fields.IntField(pk=True)
    order_id = fields.IntField(null=True)
    

    class Meta:
        table = 'socket_order'
        indexes=("order_payments", "order_id")

    def __str__(self):
        return self.order_id


class Payment(Model):
    order = fields.ForeignKeyField('models.Order', related_name='order_payments')

    class Meta:
        table = 'socket_payment'
       