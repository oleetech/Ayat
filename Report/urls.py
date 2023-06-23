from django.urls import path

from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('sales_order_list_by_date/form/', views.sales_order_list_by_date, name='sales_order_list_by_date'),
    path('sales_order_list_by_orderno/form/', views.sales_order_list_by_orderno, name='sales_order_list_by_orderno'),
    path('item_search_form', views.item_search_form, name='item_search_form'),
]