from django.urls import re_path
from .consumers import *
from .flows.userflow.consumers import UserFlowConsumers
from .flows.logging.consumers import LoggingFlowConsumers



websocket_urlpatterns = [
    re_path(r'analytics/', AnalyticsConsumers.as_asgi()),
    re_path(r'userflow/', UserFlowConsumers.as_asgi()),
    re_path(r'logging/', LoggingFlowConsumers.as_asgi()),

    
    
]