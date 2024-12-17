from django.urls import path
from .views import AddProducts, OrderProduct, Productupdate, ListProduct, CartView, OderedView


urlpatterns = [
    path('add/', AddProducts.as_view()),
    path('order/', OrderProduct.as_view()),
    path('update/', Productupdate.as_view()),
    path('product/', ListProduct.as_view()),
    path('cart/', CartView.as_view()),
    path('order/list/', OderedView.as_view()),
    path('order/list/<int:pk>/', OderedView.as_view()),

]