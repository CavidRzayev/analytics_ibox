from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json
from django.contrib.auth.models import User
from channels.db import database_sync_to_async
from tortoise import Tortoise
from django.conf import settings
from ...tortoise_models import Logging
from asgiref.sync import sync_to_async

from django.core.serializers.json import DjangoJSONEncoder


class LoggingFlowConsumers(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    async def connect(self):
        if self.scope['user'].is_manager:
            self.group_name = "managers"
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name)
        await self.accept()

    async def logging_echo_message(self, event):
        await self.send_json(event)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)