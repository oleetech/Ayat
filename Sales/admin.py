from django.contrib import admin
from django import forms

from .models import SalesOrderInfo, SalesOrderItem


class SalesOrderInfoAdminForm(forms.ModelForm):
    class Meta:
        model = SalesOrderInfo
        fields = ['OrderNumber', 'CustomerName', 'Address', 'Created', 'TotalAmount']
        widgets = {
            'OrderNumber': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.instance.pk:
            last_order = SalesOrderInfo.objects.order_by('-OrderNumber').first()
            if last_order:
                next_order_number = last_order.OrderNumber + 1
            else:
                next_order_number = 1

            self.initial['OrderNumber'] = next_order_number


class SalesOrderItemInline(admin.TabularInline):
    model = SalesOrderItem
    extra = 1  # Set the desired value for the 'extra' attribute


class SalesOrderInfoAdmin(admin.ModelAdmin):
    form = SalesOrderInfoAdminForm
    inlines = [SalesOrderItemInline]

    class Media:
        js = ('js/salesorder.js',)
        defer = True  # Add the defer attribute


admin.site.register(SalesOrderInfo, SalesOrderInfoAdmin)

from .models import DeliveryInfo, DeliveryItem
class DeliveryInfoAdminForm(forms.ModelForm):
    class Meta:
        model = DeliveryInfo
        fields = ['SalesOrder', 'CustomerName', 'Address', 'DocNo', 'TotalAmount']
        widgets = {
            'DocNo': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.instance.pk:
            last_order = DeliveryInfo.objects.order_by('-DocNo').first()
            if last_order:
                next_order_number = last_order.DocNo + 1
            else:
                next_order_number = 1

            self.initial['DocNo'] = next_order_number
            
class DeliveryItemInline(admin.TabularInline):
    model = DeliveryItem
    extra = 1  # Set the desired value for the 'extra' attribute            
    
class DeliveryInfoAdmin(admin.ModelAdmin):
    form = DeliveryInfoAdminForm
    inlines = [DeliveryItemInline]

    class Media:
        js = ('js/delivery.js',)
        defer = True  # Add the defer attribute    
        
admin.site.register(DeliveryInfo, DeliveryInfoAdmin)        