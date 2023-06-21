from django.contrib import admin
from django import forms
from django.db.models import Sum
from django.core.exceptions import ValidationError

from .models import SalesOrderInfo, SalesOrderItem


class SalesOrderInfoAdminForm(forms.ModelForm):
    class Meta:
        model = SalesOrderInfo
        fields = ['OrderNumber', 'CustomerName', 'Address', 'Created', 'TotalAmount','TotalQty']
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
        fields = ['SalesOrder', 'CustomerName', 'Address', 'DocNo', 'TotalAmount','TotalQty']
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

            

    def clean(self):
        cleaned_data = super().clean()
        sales_order = cleaned_data.get('SalesOrder')
        total_amount = cleaned_data.get('TotalAmount')
        total_qty = cleaned_data.get('TotalQty')

        # Retrieve the SalesOrderInfo instance
        try:
            sales_order_info = SalesOrderInfo.objects.get(OrderNumber=sales_order)
        except SalesOrderInfo.DoesNotExist:
            raise forms.ValidationError("Invalid Sales Order.")

        # Calculate the total amount and quantity of DeliveryInfo instances for the given SalesOrder
        delivery_info_totals = DeliveryInfo.objects.filter(SalesOrder=sales_order).aggregate(
            total_amount=Sum('TotalAmount'), total_qty=Sum('TotalQty')
        )
        delivery_info_sum_amount = delivery_info_totals.get('total_amount') or 0
        delivery_info_sum_qty = delivery_info_totals.get('total_qty') or 0

        # Calculate the remaining total amount and quantity after adding the current form's values
        remaining_total_amount = delivery_info_sum_amount + total_amount - sales_order_info.TotalAmount
        remaining_total_qty = delivery_info_sum_qty + total_qty - sales_order_info.TotalQty

        if remaining_total_amount > 0:
            raise forms.ValidationError("Total amount exceeds the allowed limit for the Sales Order.")

        if remaining_total_qty > 0:
            raise forms.ValidationError("Total quantity exceeds the allowed limit for the Sales Order.")

        return cleaned_data



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