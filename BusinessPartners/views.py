from django.shortcuts import get_object_or_404
from .models import BusinessPartner
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
@csrf_exempt
def businesspartners(request):
    if request.method == 'POST':
        customername = request.POST.get('customername')
        customer = get_object_or_404(BusinessPartner, id=customername)

        response = {
            'address': customer.address
        }
        return JsonResponse(response)
    else:
        return HttpResponse('g')

 

  

