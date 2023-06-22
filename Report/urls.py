from django.urls import path

from . import views

urlpatterns = [
    path('sales-orders/form/', views.sales_order_list, name='sales_order_form'),

]