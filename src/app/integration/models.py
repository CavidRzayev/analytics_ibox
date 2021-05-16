from tortoise import fields
from tortoise.models import Model



class Integration(Model):
    type = fields.CharField(max_length=50, null=True)
    message = fields.CharField(max_length=1000, null=True)
    content = fields.TextField(null=True)
    status = fields.CharField(max_length=100, null=True)
    timestamp = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "socket_logging_integrations"
