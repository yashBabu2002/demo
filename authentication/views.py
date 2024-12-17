from django.shortcuts import render

# Create your views here.
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse
from ecommerce.models import User
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if not username and not password:
            return JsonResponse({"error":"Username and passwords are required"}, status=400) # missing fields
        
        if password != confirm_password:
            return JsonResponse({"error":"passwords mismatch"}, status=422)  # password mismatch
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({"error":"User already exists"},  status=409) # already exists

         
        User.objects.create_user(
            username=username,
            email=email,
            phone=phone,
            password=password
        )

        return JsonResponse({"message":"user created successfully"}, status=201) # for created
        
    return JsonResponse({"error":"Invalid request method"}, status=405) # bad request (only post is allowed) 
        


@method_decorator(csrf_exempt, name='dispatch')
class Login(View):
    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']

        if not email or not password:
             return JsonResponse({"error":"username and passwords are required"}, status=400) # missing fields
        

        user = authenticate(request, email=email, password=password)

        
        if user is not None:
            login(request, user)
            return JsonResponse({"message":"user logged in successfully"}, status=200) # ok
        else:
            return JsonResponse({"error":"Invalid username and password"}, status=401) # unauthorized access
        
        

@csrf_exempt
def logoutview(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({"message":"user logged out successfully"}, status=200) # ok
        
    return JsonResponse({"error":"Invalid request method"}, status=405) # bad request

