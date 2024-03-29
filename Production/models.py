from django.db import models
from django import forms
from django.contrib import admin
from django.utils import timezone
from datetime import date

from django.forms import inlineformset_factory
from Sales.models import SalesOrderInfo,SalesOrderItem

# Create your models here.

'''
  ____    _   _   _      ___     __     __  __           _                   _           _       
 | __ )  (_) | | | |    / _ \   / _|   |  \/  |   __ _  | |_    ___   _ __  (_)   __ _  | |  ___ 
 |  _ \  | | | | | |   | | | | | |_    | |\/| |  / _` | | __|  / _ \ | '__| | |  / _` | | | / __|
 | |_) | | | | | | |   | |_| | |  _|   | |  | | | (_| | | |_  |  __/ | |    | | | (_| | | | \__ \
 |____/  |_| |_| |_|    \___/  |_|     |_|  |_|  \__,_|  \__|  \___| |_|    |_|  \__,_| |_| |___/
                                                                                                 

'''
class BillOfMaterials(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=10, decimal_places=4)

class ChildComponent(models.Model):
    bill_of_materials = models.ForeignKey(BillOfMaterials, on_delete=models.CASCADE, related_name='child_components')
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    uom = models.CharField(max_length=20)
    quantity = models.DecimalField(max_digits=10, decimal_places=4)


'''
  ____                       _                  _     _                      ___               _               
 |  _ \   _ __    ___     __| |  _   _    ___  | |_  (_)   ___    _ __      / _ \   _ __    __| |   ___   _ __ 
 | |_) | | '__|  / _ \   / _` | | | | |  / __| | __| | |  / _ \  | '_ \    | | | | | '__|  / _` |  / _ \ | '__|
 |  __/  | |    | (_) | | (_| | | |_| | | (__  | |_  | | | (_) | | | | |   | |_| | | |    | (_| | |  __/ | |   
 |_|     |_|     \___/   \__,_|  \__,_|  \___|  \__| |_|  \___/  |_| |_|    \___/  |_|     \__,_|  \___| |_|   
                                                                                                               
'''
class Production(models.Model):
    code = models.CharField(max_length=20,default='')    
    name = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=10, decimal_places=4)
    sales_order_no = models.ForeignKey(SalesOrderInfo,on_delete=models.CASCADE,related_name='sales_production_order',default=1)
    created_date = models.DateField(default=date.today)
    order_date = models.DateField(default=date.today)
    start_date = models.DateField(default=date.today)
    due_date = models.DateField(default=date.today)
    docno = models.PositiveIntegerField(unique=True,default=1)
    

        
    def __str__(self):
        return f"{self.docno}"

class ProductionComponent(models.Model):
    production = models.ForeignKey(Production, on_delete=models.CASCADE, related_name='production_components')
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    uom = models.CharField(max_length=20)
    quantity = models.DecimalField(max_digits=10, decimal_places=4)

    def __str__(self):
        return self.name   






'''
  ____                         _           _       _____                                ____                       _                  _     _                 
 |  _ \    ___    ___    ___  (_)  _ __   | |_    |  ___|  _ __    ___    _ __ ___     |  _ \   _ __    ___     __| |  _   _    ___  | |_  (_)   ___    _ __  
 | |_) |  / _ \  / __|  / _ \ | | | '_ \  | __|   | |_    | '__|  / _ \  | '_ ` _ \    | |_) | | '__|  / _ \   / _` | | | | |  / __| | __| | |  / _ \  | '_ \ 
 |  _ <  |  __/ | (__  |  __/ | | | |_) | | |_    |  _|   | |    | (_) | | | | | | |   |  __/  | |    | (_) | | (_| | | |_| | | (__  | |_  | | | (_) | | | | |
 |_| \_\  \___|  \___|  \___| |_| | .__/   \__|   |_|     |_|     \___/  |_| |_| |_|   |_|     |_|     \___/   \__,_|  \__,_|  \___|  \__| |_|  \___/  |_| |_|
                                  |_|                                                                                                                         
'''

class ProductionReceipt(models.Model):
    ReceiptNumber = models.PositiveIntegerField(default=1, unique=True)
    TotalAmount = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True,default=0)
    TotalQty = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True,default=0)  
    created_date = models.DateField(default=date.today)
    def __str__(self):
        return f"ReceiptNo{self.ReceiptNumber}"


            
            
class ProductionReceiptItem(models.Model):
    ReceiptNumber = models.ForeignKey(ProductionReceipt, on_delete=models.CASCADE, null=True, default=None)
    SalesOrderItem = models.ForeignKey(SalesOrderItem, on_delete=models.CASCADE, null=True, default=None)
    ProductionNo = models.ForeignKey(Production, on_delete=models.CASCADE, related_name='production_receipt_components', null=True)
    ItemCode = models.CharField(max_length=50,default='')
    ItemName = models.CharField(max_length=50)
    Quantity = models.PositiveIntegerField(default=0)
    Price = models.DecimalField(max_digits=10, decimal_places=4)
    PriceTotal = models.DecimalField(max_digits=10, decimal_places=4)
    Size = models.CharField(max_length=50,default='')
    Color = models.CharField(max_length=50,default='')
    def __str__(self):
        return f": {self.ReceiptNumber}"