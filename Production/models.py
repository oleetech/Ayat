from django.db import models
from django import forms
from django.contrib import admin
from django.utils import timezone
from django.forms import inlineformset_factory
from Sales.models import SalesOrderInfo,SalesOrderItem

# Create your models here.
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

class ProductionComponentInline(admin.TabularInline):
    model = ProductionComponent
    extra = 1  # Set the desired value for the 'extra' attribute
class ProductionForm(forms.ModelForm):
    docno = forms.IntegerField(disabled=True)  # Add this line to the form
    
    class Meta:
        model = Production
        fields = ['name', 'quantity', 'sales_order_no', 'docno']
        widgets = {
            'docno': forms.TextInput(attrs={'readonly': 'readonly'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if not self.instance.pk:
            # Get the last inserted docno
            last_docno = Production.objects.order_by('-docno').first()
            if last_docno:
                next_docno = last_docno.docno + 1
            else:
                next_docno = 1

            self.initial['docno'] = next_docno
            
            
            
class ProductionAdmin(admin.ModelAdmin):
    form = ProductionForm
    inlines = [ProductionComponentInline]
    class Media:
        js = ('js/fetch_sales_order_info.js',)
        defer = True  # Add the defer attribute

admin.site.register(Production, ProductionAdmin)





class ProductionReceipt(models.Model):
    ReceiptNumber = models.PositiveIntegerField(default=1, unique=True)
    OrderNumber = models.ForeignKey(SalesOrderInfo, on_delete=models.CASCADE, null=True, default=None)

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

    def __str__(self):
        return f": {self.ReceiptNumber}"