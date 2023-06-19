from django.contrib import admin
from django import forms

from .models import SalesOrderInfo, SalesOrderItem


class SalesOrderInfoAdminForm(forms.ModelForm):
    class Meta:
        model = SalesOrderInfo
        fields = '__all__'
        widgets = {
            'TotalAmount': forms.TextInput(attrs={'readonly': 'readonly'}),
        }


class SalesOrderItemInline(admin.TabularInline):
    model = SalesOrderItem


class SalesOrderInfoAdmin(admin.ModelAdmin):
    form = SalesOrderInfoAdminForm
    inlines = [SalesOrderItemInline]

    class Media:
        js = ('js/salesorder.js',)
        defer = True  # Add the defer attribute


admin.site.register(SalesOrderInfo, SalesOrderInfoAdmin)
