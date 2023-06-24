from django.urls import path
from . import views

urlpatterns = [

    path('ajax/', views.ajax_view, name='ajax_view'),
    path('receipt_production_productionno/productionno/', views.receipt_production_productionno, name='receipt_production_productionno'),

]