from tortoise import Tortoise 
from django.conf import settings
from ..tortoise_models import Logging
from .utils import parse_event
from channels.db import database_sync_to_async




class LoggingProcessing:

    def __init__(self,*args, **kwargs):
        super().__init__(**kwargs)

    async def logging_service(self,*args, **kwargs):
        await Tortoise.init(**settings.TORTOISE_INIT)
        await Tortoise.generate_schemas()
        pars_data = await parse_event(**kwargs)
        pars_data['type'] = kwargs['type']
        create_logging = await Logging.create(**pars_data)
        return create_logging
        await Tortoise.close_connections()
