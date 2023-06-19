from django.db import models
from GeneralSettings.models import Currency,Unit

# Create your models here.
class BusinessPartner(models.Model):
    code = models.CharField(max_length=50,unique=True)
    name = models.CharField(max_length=100,unique=True)
    address = models.TextField()
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT,default=1)

    CURRENCY_TYPES = [
        ('local', 'Local Currency'),
        ('foreign', 'Foreign Currency'),
    ]
    currency_type = models.CharField(max_length=10, choices=CURRENCY_TYPES,default='local')

    VENDOR_TYPES = [
        ('supplier', 'Supplier'),
        ('customer', 'Customer'),
    ]
    vendor_type = models.CharField(max_length=10, choices=VENDOR_TYPES,default='customer')

    def __str__(self):
        return self.name  