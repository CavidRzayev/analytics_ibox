from django.urls import path
from .views import *
urlpatterns = [
    path('room', index),
    path('order/<str:order_id>/', order, name='order'),
]
