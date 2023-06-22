from django.shortcuts import render
from Sales.models import SalesOrderInfo,SalesOrderItem
from .forms import SalesOrderForm





def sales_order_list(request):
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
