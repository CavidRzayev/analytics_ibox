from django.urls import path
from .views import *
urlpatterns = [
    path('order/', order, name='order'),
    path('', logins, name='login'),
    path('logout',logout_view,name="logout"),
    path('order/<int:order_id>/', order_detail, name='order_detail'),
    path('logging/',logging,name="logging"),
    path('logging-payment/',logging_payment,name="logging_payment"),
]
