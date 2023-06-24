from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import BusinessPartner
# Create your views here.
@csrf_exempt
def businesspartners(request):
    if request.method == 'POST':
        customername = request.POST.get('customername')
        customer = get_object_or_404(BusinessPartner.objects, name=customername)

        response = {
            'address': customer.address
        }
        return JsonResponse(response)
    else:
       return HttpResponse('g')

 

  

