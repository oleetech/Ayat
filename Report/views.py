from django.shortcuts import render, get_object_or_404, redirect
from Sales.models import SalesOrderInfo,SalesOrderItem
from ItemMasterData.models import Item,Stock,ItemReceipt,ItemDelivery,Warehouse
from .forms import SalesOrderForm,SalesOrderNumberForm,SearchForm,ItemForm
from django.db.models import Q,Sum


def index(request):
     return render(request,'index.html')

def sales_order_list_by_date(request):
    if request.method == 'POST':
        form = SalesOrderForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            
            sales_orders = SalesOrderInfo.objects.filter(Created__range=[start_date, end_date])
            sales_order_items = SalesOrderItem.objects.filter(OrderNumber__in=sales_orders)
            
            return render(request, 'sales_order_list.html', {'sales_orders': sales_orders, 'sales_order_items': sales_order_items})
    else:
        form = SalesOrderForm()

    return render(request, 'sales_order_form.html', {'form': form})

def sales_order_list_by_orderno(request):
    if request.method == 'POST':
        form = SalesOrderNumberForm(request.POST)
        if form.is_valid():
            order_number = form.cleaned_data['order_number']
            
            sales_orders = SalesOrderInfo.objects.filter(OrderNumber=order_number)
            sales_order_items = SalesOrderItem.objects.filter(OrderNumber__in=sales_orders)
            
            return render(request, 'sales_order_list.html', {'sales_orders': sales_orders, 'sales_order_items': sales_order_items})
    else:
        form = SalesOrderNumberForm()

    return render(request, 'sales_order_form.html', {'form': form})

def item_search_form(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)   
        if form.is_valid():
            name = request.POST.get('name')
            description = request.POST.get('description')
            results = Item.objects.filter(
                Q(name__icontains=name) ,
                Q(description__icontains=description) 
                # Add more conditions for other columns as necessary
            )            
            if results.count() == 1:
                item = results.first()
                warehouses = Warehouse.objects.all()
                item_quantities = []
                for warehouse in warehouses:
                    stock_quantity = Stock.objects.filter(warehouse=warehouse, item=item).aggregate(Sum('quantity'))['quantity__sum'] or 0
                    receipt_quantity = ItemReceipt.objects.filter(warehouse=warehouse, item=item).aggregate(Sum('quantity'))['quantity__sum'] or 0
                    delivery_quantity = ItemDelivery.objects.filter(warehouse=warehouse, item=item).aggregate(Sum('quantity'))['quantity__sum'] or 0

                    total_quantity = stock_quantity + receipt_quantity - delivery_quantity

                    item_quantities.append({
                        'warehouse': warehouse,
                        'quantity': total_quantity,
                    })                
                form = ItemForm(instance=item)
                return render(request, 'item/item_detail.html', {'form': form, 'item': item,  'item_quantities': item_quantities})
            else:
                return render(request, 'item/search_results.html', {'results': results})
        else:
            pass
    else:
        form = SearchForm()
        context = {
            'form': form,
        }
    return render(request, 'item/search_form.html',context)


def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    warehouses = Warehouse.objects.all()
    item_quantities = []
    form = ItemForm(instance=item)
    for warehouse in warehouses:
        stock_quantity = Stock.objects.filter(warehouse=warehouse, item=item).aggregate(Sum('quantity'))['quantity__sum'] or 0
    receipt_quantity = ItemReceipt.objects.filter(warehouse=warehouse, item=item).aggregate(Sum('quantity'))['quantity__sum'] or 0
    delivery_quantity = ItemDelivery.objects.filter(warehouse=warehouse, item=item).aggregate(Sum('quantity'))['quantity__sum'] or 0

    total_quantity = stock_quantity + receipt_quantity - delivery_quantity

    item_quantities.append({
        'warehouse': warehouse,
        'quantity': total_quantity,
    })
    
    return render(request, 'item/item_detail.html', {'form': form, 'item': item,  'item_quantities': item_quantities})
