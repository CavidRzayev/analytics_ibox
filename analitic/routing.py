from channels.auth import AuthMiddleware,AuthMiddlewareStack
from django.urls import path  
from channels.routing import *
from sockets.routing import websocket_urlpatterns
import sockets
from .utils import TokenAuthMiddleware


application = ProtocolTypeRouter({
    'websocket': TokenAuthMiddleware(
        AuthMiddlewareStack(
        URLRouter(
            sockets.routing.websocket_urlpatterns 
            
        )
    ),
)
})