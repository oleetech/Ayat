from django.urls import path
from . import views

urlpatterns = [
    path('orderinfo/',views.orderinfo,name='orderinfo'),
]