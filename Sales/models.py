from django.db import models
from django.utils import timezone
from django import forms
from BusinessPartners.models import BusinessPartner 
# Create your models here.
from ItemMasterData.models import Item

from django.db import models
from django.utils import timezone
'''
  ____            _                   ___               _               
 / ___|    __ _  | |   ___   ___     / _ \   _ __    __| |   ___   _ __ 
 \___ \   / _` | | |  / _ \ / __|   | | | | | '__|  / _` |  / _ \ | '__|
  ___) | | (_| | | | |  __/ \__ \   | |_| | | |    | (_| | |  __/ | |   
 |____/   \__,_| |_|  \___| |___/    \___/  |_|     \__,_|  \___| |_|   
                                                                        
'''
class SalesOrderInfo(models.Model):
    OrderNumber = models.PositiveIntegerField(default=1, unique=True)
    CustomerName = models.ForeignKey(BusinessPartner, on_delete=models.CASCADE, null=True, default=None)
    Address = models.CharField(max_length=50)
    Created = models.DateTimeField(default=timezone.now)
    TotalAmount = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True,default=0)


    def __str__(self):
        return f"SalesOrderNo{self.OrderNumber}"




class SalesOrderItem(models.Model):
    OrderNumber = models.ForeignKey(SalesOrderInfo, on_delete=models.CASCADE, null=True, default=None)
    ItemCode = models.CharField(max_length=20)
    ItemName = models.CharField(max_length=50)
    Quantity = models.PositiveIntegerField(default=0)
    Price = models.DecimalField(max_digits=10, decimal_places=4)
    PriceTotal = models.DecimalField(max_digits=10, decimal_places=4)

    def __str__(self):
        return f": {self.OrderNumber}"

'''
  ____           _   _                               
 |  _ \    ___  | | (_) __   __   ___   _ __   _   _ 
 | | | |  / _ \ | | | | \ \ / /  / _ \ | '__| | | | |
 | |_| | |  __/ | | | |  \ V /  |  __/ | |    | |_| |
 |____/   \___| |_| |_|   \_/    \___| |_|     \__, |
                                               |___/ 
'''

class DeliveryInfo(models.Model):
    SalesOrder = models.PositiveIntegerField(primary_key=True)
    CustomerName = models.ForeignKey(BusinessPartner, on_delete=models.CASCADE, null=True, default=None)
    Address = models.CharField(max_length=50)
    Created = models.DateTimeField(default=timezone.now)
    DocNo = models.PositiveIntegerField(unique=True,default=1)
    TotalAmount = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True,default=0)
   
    def __str__(self):
        return f"Delivery for SalesOrderNo {self.DocNo}"


class DeliveryItem(models.Model):
    SalesOrder = models.PositiveIntegerField(default=1)    
    Delivery = models.ForeignKey(DeliveryInfo, on_delete=models.CASCADE)
    ItemCode = models.CharField(max_length=20)
    ItemName = models.CharField(max_length=50)
    Quantity = models.PositiveIntegerField(default=0)
    Price = models.DecimalField(max_digits=10, decimal_places=4)
    PriceTotal = models.DecimalField(max_digits=10, decimal_places=4)
    def __str__(self):
        return f"{self.SalesOrder}"
