from django.http import JsonResponse
from ecommerce.models import User

def validate_registration(**kwargs):
    username = kwargs.get('username')
    email = kwargs.get('email')
    password = kwargs.get('password')
    confirm_password = kwargs.get('confirm_password')
    phone = kwargs.get('phone')

    if username is None:
        return JsonResponse({'success':False, 'error':'Username field is required'}, status=400)
    
    if email is None:
        return JsonResponse({'success':False, 'error':'Email field is required'}, status=400)
    
    if password is None:
        return JsonResponse({'success':False, 'error':'Password field is required'}, status=400)
    
    if phone is None:
        return JsonResponse({'success':False, 'error':'Phone field is required'}, status=400)
    
    if User.objects.filter(username=username).exists():
        return JsonResponse({'success':False, 'error':'Username already exists , please try another name'}, status=400)
    
    if User.objects.filter(email=email).exists():
        return JsonResponse({'success':False, 'error':'Email already exists'}, status=400)

    if password != confirm_password:
        return JsonResponse({'success':False, 'error':'Confirm password does not match'}, status=400)
    

        
    
def validate_login(**kwargs):
    email = kwargs.get('email')
    print(email)
    password = kwargs.get('password')

    if email is None:
        return JsonResponse({'success':False, 'error':'Please enter your email'}, status=400) 
    
    if password is None:
        return JsonResponse({'success':False, 'error':'Please enter your password'}, status=400) 

