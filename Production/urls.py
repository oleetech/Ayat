from django.urls import path
from .views import ajax_view

urlpatterns = [

    path('ajax/', ajax_view, name='ajax_view'),

]