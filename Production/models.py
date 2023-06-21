from django.db import models
from django import forms
from django.contrib import admin
from django.utils import timezone
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
    bomtype = models.CharField(max_length=20)
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
    name = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=10, decimal_places=4)
    sales_order_no = models.ForeignKey(SalesOrderInfo,on_delete=models.CASCADE,related_name='sales_production_order',default=1)
    created_date = models.DateTimeField(default=timezone.now)
    order_date = models.DateField(default=timezone.now)
    start_date = models.DateField(default=timezone.now)
    due_date = models.DateField(default=timezone.now)
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

    # Define a method to create formset instances from form data
    @classmethod
    def create_from_formset(cls, formset_data):
        components = []
        for data in formset_data:
            component = cls(
                code=data['code'],
                name=data['name'],
                uom=data['uom'],
                quantity=data['quantity']
            )
            components.append(component)
        return cls.objects.bulk_create(components)


    # Update your view function to handle multiple formsets
    def save_production_components(request):
        if request.method == 'POST':
            formset_data = request.POST.getlist('formset_data[]')
            components = ProductionComponent.create_from_formset(formset_data)
            # Process or perform any additional operations on the saved components
            return HttpResponse('Formsets saved successfully')
        else:
            return HttpResponseBadRequest('Invalid request method')


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
    OrderNumber = models.ForeignKey(SalesOrderInfo, on_delete=models.CASCADE, null=True, default=None)
    TotalAmount = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True,default=0)
    def __str__(self):
        return f"ReceiptNo{self.ReceiptNumber}"


            
            
class ProductionReceiptItem(models.Model):
    ReceiptNumber = models.ForeignKey(ProductionReceipt, on_delete=models.CASCADE, null=True, default=None)
    SalesOrderItem = models.ForeignKey(SalesOrderItem, on_delete=models.CASCADE, null=True, default=None)
    ProductionNo = models.ForeignKey(Production, on_delete=models.CASCADE, related_name='production_receipt_components', null=True)
    ItemName = models.CharField(max_length=50)
    Quantity = models.PositiveIntegerField(default=0)
    Price = models.DecimalField(max_digits=10, decimal_places=4)
    PriceTotal = models.DecimalField(max_digits=10, decimal_places=4)
    Size = models.CharField(max_length=50,default='')
    Color = models.CharField(max_length=50,default='')
    def __str__(self):
        return f": {self.ReceiptNumber}"