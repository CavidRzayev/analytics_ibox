from tortoise import fields
from tortoise.models import Model
from .defaultmodel import DefaultModel



class Order(DefaultModel):
    order_id = fields.IntField(null=True)
    payment_id = fields.IntField(null=True)

    class Meta:
        table = 'socket_order'
        indexes=("order_id","payment_id",)

    def __str__(self):
        return str(self.id)