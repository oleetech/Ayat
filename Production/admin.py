from django.contrib import admin
from django import forms
from django.forms import inlineformset_factory
from ItemMasterData.models import Item
from django.contrib.admin import widgets
from Sales.models import SalesOrderInfo,SalesOrderItem

'''
   ___    _   _   _      ___     __     __  __           _                   _           _       
 | __ )  (_) | | | |    / _ \   / _|   |  \/  |   __ _  | |_    ___   _ __  (_)   __ _  | |  ___ 
 |  _ \  | | | | | |   | | | | | |_    | |\/| |  / _` | | __|  / _ \ | '__| | |  / _` | | | / __|
 | |_) | | | | | | |   | |_| | |  _|   | |  | | | (_| | | |_  |  __/ | |    | | | (_| | | | \__ \
 |____/  |_| |_| |_|    \___/  |_|     |_|  |_|  \__,_|  \__|  \___| |_|    |_|  \__,_| |_| |___/
                                                                                                 
'''
from .models import BillOfMaterials, ChildComponent
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


'''
  ____                       _                  _     _                      ___               _               
 |  _ \   _ __    ___     __| |  _   _    ___  | |_  (_)   ___    _ __      / _ \   _ __    __| |   ___   _ __ 
 | |_) | | '__|  / _ \   / _` | | | | |  / __| | __| | |  / _ \  | '_ \    | | | | | '__|  / _` |  / _ \ | '__|
 |  __/  | |    | (_) | | (_| | | |_| | | (__  | |_  | | | (_) | | | | |   | |_| | | |    | (_| | |  __/ | |   
 |_|     |_|     \___/   \__,_|  \__,_|  \___|  \__| |_|  \___/  |_| |_|    \___/  |_|     \__,_|  \___| |_|   
                                                                                                               
'''
from .models import Production, ProductionComponent

class ProductionComponentInline(admin.TabularInline):
    model = ProductionComponent
    extra = 1  # Set the desired value for the 'extra' attribute
class ProductionForm(forms.ModelForm):
    docno = forms.IntegerField(disabled=True)  # Add this line to the form
    code = forms.ChoiceField(choices=[])
    
    class Meta:
        model = Production
        fields = ['code','name', 'quantity', 'sales_order_no', 'docno']
        widgets = {
            'docno': forms.TextInput(attrs={'readonly': 'readonly'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['code'].choices = [(item.code, item.code) for item in Item.objects.all()]
        
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
'''
  ____                         _           _       _____                                ____                       _                  _     _                 
 |  _ \    ___    ___    ___  (_)  _ __   | |_    |  ___|  _ __    ___    _ __ ___     |  _ \   _ __    ___     __| |  _   _    ___  | |_  (_)   ___    _ __  
 | |_) |  / _ \  / __|  / _ \ | | | '_ \  | __|   | |_    | '__|  / _ \  | '_ ` _ \    | |_) | | '__|  / _ \   / _` | | | | |  / __| | __| | |  / _ \  | '_ \ 
 |  _ <  |  __/ | (__  |  __/ | | | |_) | | |_    |  _|   | |    | (_) | | | | | | |   |  __/  | |    | (_) | | (_| | | |_| | | (__  | |_  | | | (_) | | | | |
 |_| \_\  \___|  \___|  \___| |_| | .__/   \__|   |_|     |_|     \___/  |_| |_| |_|   |_|     |_|     \___/   \__,_|  \__,_|  \___|  \__| |_|  \___/  |_| |_|
                                  |_|                                                                                                                         
'''
from .models import ProductionReceipt, ProductionReceiptItem

            
class ProductionReceiptForm(forms.ModelForm):
    ReceiptNumber = forms.IntegerField(disabled=True)
    TotalQty = forms.DecimalField(max_digits=10, decimal_places=4)
    TotalAmount = forms.DecimalField(max_digits=10, decimal_places=4)

    class Meta:
        model = ProductionReceipt
        fields = ['ReceiptNumber', 'TotalAmount','TotalQty']

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
    fields = ('ProductionNo','ReceiptNumber','ItemCode', 'ItemName','Size', 'Color' ,'Quantity','Price', 'PriceTotal')

class ProductionReceiptAdmin(admin.ModelAdmin):
    inlines = [ProductionReceiptItemInline]
    form = ProductionReceiptForm
    class Media:
        js = ('js/receiptfromproduction.js',)
        defer = True  # Add the defer attribute
    

admin.site.register(ProductionReceipt, ProductionReceiptAdmin)