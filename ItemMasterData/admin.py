from django.contrib import admin
from django import forms
from django.forms import inlineformset_factory

from django.contrib.admin import widgets
from .models import Warehouse, Item, Stock, ItemReceiptinfo, ItemReceipt, ItemDeliveryinfo, ItemDelivery

class ItemReceiptInline(admin.TabularInline):
    model = ItemReceipt
    extra = 1
class ItemReceiptinfoForm(forms.ModelForm):
    docno = forms.IntegerField(disabled=True)  # Add this line to the form
    
    class Meta:
        model = ItemReceiptinfo
        fields = [ 'docno', 'created']
        widgets = {
            'docno': forms.TextInput(attrs={'readonly': 'readonly'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if not self.instance.pk:
            # Get the last inserted docno
            last_docno = ItemReceiptinfo.objects.order_by('-docno').first()
            if last_docno:
                next_docno = last_docno.docno + 1
            else:
                next_docno = 1

            self.initial['docno'] = next_docno        

@admin.register(ItemReceiptinfo)
class ItemReceiptinfoAdmin(admin.ModelAdmin):
    form = ItemReceiptinfoForm
    inlines = [ItemReceiptInline]

class ItemDeliveryInline(admin.TabularInline):
    model = ItemDelivery
    extra = 1

class ItemDeliveryinfoForm(forms.ModelForm):
    docno = forms.IntegerField(disabled=True)  # Add this line to the form
    
    class Meta:
        model = ItemDeliveryinfo
        fields = [ 'docno', 'created']
        widgets = {
            'docno': forms.TextInput(attrs={'readonly': 'readonly'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if not self.instance.pk:
            # Get the last inserted docno
            last_docno = ItemReceiptinfo.objects.order_by('-docno').first()
            if last_docno:
                next_docno = last_docno.docno + 1
            else:
                next_docno = 1

            self.initial['docno'] = next_docno    


@admin.register(ItemDeliveryinfo)
class ItemDeliveryinfoAdmin(admin.ModelAdmin):
    form = ItemDeliveryinfoForm
    inlines = [ItemDeliveryInline]

# Register the other models normally
admin.site.register(Warehouse)
admin.site.register(Item)
admin.site.register(Stock)

