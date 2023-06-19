from django.db import models
from django.utils import timezone
from BusinessPartners.models import BusinessPartner 
# Create your models here.


from django.db import models
from django.utils import timezone

class SalesOrderInfo(models.Model):
    OrderNumber = models.PositiveIntegerField(default=1, unique=True)
    CustomerName = models.ForeignKey(BusinessPartner, on_delete=models.CASCADE, null=True, default=None)
    Address = models.CharField(max_length=50)
    Created = models.DateTimeField(default=timezone.now)
    TotalAmount = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True,default=0)


    def __str__(self):
        return f"SalesOrderInfo: {self.OrderNumber}"

class SalesOrderItem(models.Model):
    OrderNumber = models.ForeignKey(SalesOrderInfo, on_delete=models.CASCADE, null=True, default=None)
    ItemCode = models.CharField(max_length=20)
    ItemName = models.CharField(max_length=50)
    Quantity = models.PositiveIntegerField(default=0)
    Price = models.DecimalField(max_digits=10, decimal_places=4)
    PriceTotal = models.DecimalField(max_digits=10, decimal_places=4)

    def __str__(self):
        return f": {self.OrderNumber}"

