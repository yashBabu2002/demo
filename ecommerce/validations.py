
from django.http import JsonResponse

def validate(**kwargs):
    status = kwargs.get('status')
    ordered_status = kwargs.get('ordered_status')

    if status == 'confirmed': 
        if ordered_status == 'confirmed':
            return JsonResponse({'success':False, 'error':'Only pending status can be updated as confirmed'}, status=400)

    if status == 'shipped':
        if ordered_status == 'shipped':
            return JsonResponse({'success':False, 'error':'Only confirmed status can be updated as shipped'}, status=400)

    if status == 'delivered':
        if ordered_status == 'delivered':
            return JsonResponse({'success':False, 'error':'Only shipped status can be updated as delivered'}, status=400)
        
    
def validate_product(**kwargs):
    name = kwargs.get('name')
    description = kwargs.get('description')
    stock_quantity = kwargs.get('stock_quantity')
    price = kwargs.get('price')

    if name is None:
        return JsonResponse({'success':False, 'error':'Product name field is required'}, status=400)
    
    if description is None:
        return JsonResponse({'success':False, 'error':'description field is required'}, status=400)
    
    if stock_quantity is None:
        return JsonResponse({'success':False, 'error':'stock_quantity field is required'}, status=400)
    elif stock_quantity <= 0:
        return JsonResponse({'success':False, 'error':'stock quantity must be greater than 0'}, status=400)
    
    if price is None:
        return JsonResponse({'success':False, 'error':'price field is required'}, status=400)
    elif price <= 0:
        return JsonResponse({'success':False, 'error':'Product price must be greater than 0'}, status=400)

    

