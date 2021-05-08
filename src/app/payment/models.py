from tortoise import fields
from tortoise.models import Model
from tortoise.signals import post_delete, post_save, pre_delete, pre_save
from src.app.default.models import DefaultModel



class Payment(DefaultModel):
    order = fields.ForeignKeyField('models.Order', related_name='order_payments')

    class Meta:
        table = 'socket_payment'
    