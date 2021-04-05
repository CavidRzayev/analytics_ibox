from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token


@database_sync_to_async
def get_user(query_string):
    try:
        query = query_string.decode().split('=')
        token_name, token_key = query
        if token_name == 'authorization':
            token = Token.objects.get(key=token_key)
            return token.user, True
    except Token.DoesNotExist:
        return AnonymousUser(), False


class TokenAuthMiddleware:

    def __init__(self, inner):
        self.inner = inner
        

    def __call__(self, scope):
        return TokenAuthMiddlewareInstance(scope, self)


class TokenAuthMiddlewareInstance:
   
    def __init__(self, scope, middleware,notauth=0):
        self.middleware = middleware
        self.scope = dict(scope)
        self.inner = self.middleware.inner
        self.notauth = notauth

    async def __call__(self, receive, send):
        query_string = self.scope['query_string']
        if b'authorization' in query_string:
            user =  await get_user(query_string)
            self.scope['auth'] = user[1]
            self.scope['user'] =  user[0]
            return await self.inner(self.scope,receive, send)


TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))