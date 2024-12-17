
from django.http import JsonResponse

def validate(**kwargs):
    if kwargs.get('status') == "confirmed": 
        if kwargs.get('ordered_status') == kwargs.get('status'):
            return JsonResponse({"error":"Only pending status can be updated as confirmed"})

    if kwargs.get('status') == 'shipped':
        if kwargs.get('ordered_status') == kwargs.get('status'):
            return JsonResponse({"error":"Only confirmed status can be updated as shipped"})

    if kwargs.get('status') == 'delivered':
        if kwargs.get('ordered_status') == kwargs.get('status'):
            return JsonResponse({"error":"Only shipped status can be updated as delivered"})
        
    
        