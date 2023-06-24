from django.shortcuts import get_object_or_404
from .models import SalesOrderInfo
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
@csrf_exempt
def orderinfo(request):
    if request.method == 'POST':
        orderno = request.POST.get('orderno')
        salesorder = get_object_or_404(SalesOrderInfo, OrderNumber=orderno)

        response = {
            'Address': salesorder.Address,
            'CustomerName':salesorder.CustomerName.name,
            
        }
        return JsonResponse(response)
    else:
        return HttpResponse('g')