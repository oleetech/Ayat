from django.db import models
from django import forms
from django.contrib import admin
from django.utils import timezone
from django.forms import inlineformset_factory
from Sales.models import SalesOrderInfo

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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.docno:
            last_docno = Production.objects.order_by('-id').values_list('docno', flat=True).first()
            self.docno = last_docno + 1 if last_docno is not None else 1

    def save(self, *args, **kwargs):
        if not self.docno:
            last_docno = Production.objects.order_by('-id').values_list('docno', flat=True).first()
            self.docno = last_docno + 1 if last_docno is not None else 1
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name

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

class ProductionForm(forms.ModelForm):
    class Meta:
        model = Production
        fields = ['name', 'quantity', 'sales_order_no', 'docno']
        widgets = {
            'docno': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

class ProductionAdmin(admin.ModelAdmin):
    form = ProductionForm
    inlines = [ProductionComponentInline]
    class Media:
        js = ('js/fetch_sales_order_info.js',)
        defer = True  # Add the defer attribute

admin.site.register(Production, ProductionAdmin)
