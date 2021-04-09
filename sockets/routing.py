from django.urls import re_path
from .consumers import *
from .flows.userflow import consumers


websocket_urlpatterns = [
    re_path(r'analytics/', AnalyticsConsumers.as_asgi()),
    re_path(r'userflow/', consumers.UserFlowConsumers.as_asgi()),
    
    
]