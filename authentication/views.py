from django.shortcuts import render

# Create your views here.
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse
from ecommerce.models import User
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .auth_validations import validate_registration, validate_login
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import json

@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'success':False, 'error':'Invalid json'}, status=400)
        
        username = data.get('username')
        email = data.get('email')
        phone = data.get('phone')
        another_number = data.get('another_number', None)
        password = data.get('password')
        confirm_password = data.get('confirm_password')


        validate = validate_registration(username=username,
                                         email=email,
                                         password=password,
                                         confirm_password=confirm_password,
                                         phone=phone)
        if validate:
            return validate
        try:
            validate_password(password)
        except ValidationError as e:
            return JsonResponse({'success':False, 'error':e.messages},status=400)
        

        User.objects.create_user(
            username=username,
            email=email,
            password=password,
            phone=phone,
            another_number=another_number
        )

        return JsonResponse({'success':True, 'message':'user created successfully'}, status=201) 
        
    return JsonResponse({'success':False, 'error':'Invalid request method'}, status=405) 
        


@csrf_exempt
def login_view(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success':False, 'error':'Invalid Json'}, status=400)

    email = data.get('email')
    password = data.get('password')

    # data = json.loads(request.body)
    # email = data.get('email')
    # password = data.get('password')

    validate = validate_login(email=email, password=password)

    if validate:
        return validate        

    user = authenticate(request, email=email, password=password)

    
    if user is not None:
        login(request, user)
        return JsonResponse({'success':True, 'message':'user logged in successfully'}, status=200)
    else:
        return JsonResponse({'success':False, 'error':'Invalid username and password'}, status=401) 
    
        

@csrf_exempt
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'success':True, 'message':'user logged out successfully'}, status=200) 
        
    return JsonResponse({'success':False, 'error':'Invalid request method'}, status=405)

