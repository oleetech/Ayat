from django.contrib import admin
from .models import Warehouse, Item, Stock, ItemReceiptinfo, ItemReceipt, ItemDeliveryinfo, ItemDelivery

class ItemReceiptInline(admin.TabularInline):
    model = ItemReceipt
    extra = 1

class ItemReceiptinfoAdmin(admin.ModelAdmin):
    inlines = [ItemReceiptInline]

@admin.register(ItemReceiptinfo)
class ItemReceiptinfoAdmin(admin.ModelAdmin):
    inlines = [ItemReceiptInline]

class ItemDeliveryInline(admin.TabularInline):
    model = ItemDelivery
    extra = 1

class ItemDeliveryinfoAdmin(admin.ModelAdmin):
    inlines = [ItemDeliveryInline]

@admin.register(ItemDeliveryinfo)
class ItemDeliveryinfoAdmin(admin.ModelAdmin):
    inlines = [ItemDeliveryInline]

# Register the other models normally
admin.site.register(Warehouse)
admin.site.register(Item)
admin.site.register(Stock)

