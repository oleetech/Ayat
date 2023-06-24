from django.urls import path
from . import views

urlpatterns = [
    path('businespartnername/',views.businesspartners,name='BusinessPartnersInfo'),
]