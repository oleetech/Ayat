from django.contrib import admin
from django.forms import inlineformset_factory
from .models import (
    BillOfMaterials,
    ChildComponent,
    Production, 
    ProductionComponent
)

# Bill Of Materials 
class ChildComponentInline(admin.TabularInline):
    model = ChildComponent
class BillOfMaterialsAdmin(admin.ModelAdmin):
    inlines = [ChildComponentInline]
admin.site.register(BillOfMaterials, BillOfMaterialsAdmin)


# Production Order
class ProductionComponentInline(admin.TabularInline):
    model = ProductionComponent
class ProductionAdmin(admin.ModelAdmin):
    inlines = [ProductionComponentInline]
    class Media:
        js = ('js/fetch_sales_order_info.js',)
        defer = True  # Add the defer attribute
admin.site.register(Production, ProductionAdmin)