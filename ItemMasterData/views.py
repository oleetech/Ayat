from django.shortcuts import get_object_or_404
from .models import Item
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
@csrf_exempt
def item(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        item = get_object_or_404(Item, code=code)

        response = {
            'name': item.name
        }
        return JsonResponse(response)
    else:
        return HttpResponse('g')