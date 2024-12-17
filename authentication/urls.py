from django.urls import path
from .views import register, Login, logoutview

urlpatterns = [
    path('register/', register, name='register'),
    path('login/',Login.as_view(), name='login'),
    path('logout/', logoutview, name='logout'),

]