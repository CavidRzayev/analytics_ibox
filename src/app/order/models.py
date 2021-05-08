from tortoise import fields
from tortoise.models import Model
from src.app.default.models import DefaultModel



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
        table = "socket_order"
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