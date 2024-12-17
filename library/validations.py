from django.http import JsonResponse

def check_validate(**fields):
    if not fields.get('title'):
        return JsonResponse({"error":"Title field is required"}) 
    
    if not fields.get('author'):
        return JsonResponse({"error":"Author field is required"})
    
    if not fields.get('price'):
        return JsonResponse({"error":"Price field is required"})
    
    if not fields.get('published_year'):
        return JsonResponse({"error":"Published_year is required"})

    
    
