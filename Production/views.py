from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import BillOfMaterials,Production
@csrf_exempt
def ajax_view(request):
    if request.method == 'POST':
        production_name  = request.POST.get('name')
        production_quantity  = request.POST.get('quantity')
        bill_of_materials = BillOfMaterials.objects.filter(name=production_name).first()
        if bill_of_materials:
            child_components = bill_of_materials.child_components.all()
            updated_components = []



            for component in child_components:
                if bill_of_materials.quantity == production_quantity:
                    updated_quantity = float(component.quantity)
                else:
                    updated_quantity = float(component.quantity) * (float(production_quantity) / float(bill_of_materials.quantity))
                updated_quantity = format(updated_quantity, '.4f')
                updated_components.append({
                    'id': component.id,
                    'code': component.code,
                    'name': component.name,
                    'uom': component.uom,
                    'quantity': updated_quantity
                })
                    

        return JsonResponse(updated_components, safe=False)

    return JsonResponse([], safe=False)
# Create your views here.
@csrf_exempt
def receipt_production_productionno(request):
    if request.method == 'POST':
        production_no = request.POST.get('ProductionNo')
        production = get_object_or_404(Production, docno=production_no)
        
        response = {
            'code': production.code,
            'name': production.name,
            'quantity': str(production.quantity)  # Convert quantity to a string if needed
        }
        return JsonResponse(response)
    else:
        # Handle GET requests if needed
        pass