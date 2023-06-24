from os import name
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from GeneralSettings.models import Unit
from django.db.models import Q,Sum
# Create your models here.
class Warehouse(models.Model):
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=100)
    # Add any other fields for the Warehouse model

    def __str__(self):
        return self.name


class Item(models.Model):
    code = models.CharField(max_length=25, unique=True,default='')
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, default=1)
    unit = models.ForeignKey(Unit, on_delete=models.SET_DEFAULT, default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Add any other fields you need
    @property
    def inhand(self):
        stock_quantity = self.stock_set.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
        receipt_quantity = self.itemreceipt_set.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
        delivery_quantity = self.itemdelivery_set.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0

        return  stock_quantity + receipt_quantity - delivery_quantity
    def __str__(self):
        return self.name


class Stock(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)


class ItemReceiptinfo(models.Model):
    docno = models.PositiveIntegerField(default=1, unique=True)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return " {}".format(self.docno)


class ItemReceipt(models.Model):
    item_info = models.ForeignKey(ItemReceiptinfo, on_delete=models.CASCADE, null=True, default=None)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return " {}".format(self.item_info.docno)

    def clean(self):
        if self.quantity == 0:
            raise ValidationError("Quantity cannot be 0.")


class ItemDeliveryinfo(models.Model):
    docno = models.PositiveIntegerField(default=1, unique=True)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return " {}".format(self.docno)


class ItemDelivery(models.Model):
    item_info = models.ForeignKey(ItemDeliveryinfo, on_delete=models.CASCADE, null=True, default=None)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "ItemDelivery: {} - {}".format(self.item.name, self.quantity)
