from tortoise import fields
from tortoise.models import Model


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