from django.contrib import admin
from django import forms
from django.forms import inlineformset_factory
from .models import BillOfMaterials, ChildComponent
from django.contrib.admin import widgets
from Sales.models import SalesOrderInfo,SalesOrderItem
class ChildComponentInline(admin.TabularInline):
    model = ChildComponent
    extra = 1

ChildComponentFormSet = inlineformset_factory(
    BillOfMaterials,
    ChildComponent,
    fields=('code', 'name', 'uom', 'quantity'),
    can_delete=True,
    extra=1,
)

class BillOfMaterialsAdmin(admin.ModelAdmin):
    inlines = [ChildComponentInline]

admin.site.register(BillOfMaterials, BillOfMaterialsAdmin)



from .models import ProductionReceipt, ProductionReceiptItem

            
class ProductionReceiptForm(forms.ModelForm):
    ReceiptNumber = forms.IntegerField(disabled=True)
    OrderNumber = forms.ModelChoiceField(queryset=SalesOrderInfo.objects.all(), empty_label=None)
    TotalAmount = forms.DecimalField(max_digits=10, decimal_places=4)

    class Meta:
        model = ProductionReceipt
        fields = ['ReceiptNumber', 'TotalAmount','OrderNumber']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if not self.instance.pk:
            # Get the last inserted ReceiptNumber
            last_receipt_number = ProductionReceipt.objects.order_by('-ReceiptNumber').first()
            if last_receipt_number:
                next_receipt_number = last_receipt_number.ReceiptNumber + 1
            else:
                next_receipt_number = 1

            self.initial['ReceiptNumber'] = next_receipt_number            
            

class ProductionReceiptItemInline(admin.TabularInline):
    model = ProductionReceiptItem
    extra = 1
    fields = ('ProductionNo','ReceiptNumber', 'ItemName','Size', 'Color' ,'Quantity','Price', 'PriceTotal')

class ProductionReceiptAdmin(admin.ModelAdmin):
    inlines = [ProductionReceiptItemInline]
    form = ProductionReceiptForm
    class Media:
        js = ('js/receiptfromproduction.js',)
        defer = True  # Add the defer attribute
    

admin.site.register(ProductionReceipt, ProductionReceiptAdmin)