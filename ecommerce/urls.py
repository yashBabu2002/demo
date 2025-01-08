from django.urls import path
from .views import AddProducts, OrderProduct, Productupdate, ListProduct, CartView, OderedView, UserProfile, UpdateOrderedStatus


# urlpatterns = [
#     path('user/', UserProfile.as_view()),
#     path('add/', AddProducts.as_view()),
#     path('order/', OrderProduct.as_view()),
#     path('update/', Productupdate.as_view()),
#     path('product/', ListProduct.as_view()),
#     path('cart/', CartView.as_view()),
#     path('order/list/', OderedView.as_view()),
#     path('order/list/<int:pk>/', OderedView.as_view()),
# ]

urlpatterns = [
    path('user/', UserProfile.as_view(), name='user_profile'),
    path('add/', AddProducts.as_view(), name='add_products'),
    path('order/', OrderProduct.as_view(), name='order_product'),
    path('update/', Productupdate.as_view(), name='product_update'),
    path('product/', ListProduct.as_view(), name='list_product'),
    path('cart/', CartView.as_view(), name='cart_view'),
    path('cart/<int:pk>/', CartView.as_view(), name='cart_view'),
    path('order/list/', OderedView.as_view(), name='ordered_view'),
    path('order/list/<int:pk>/', OderedView.as_view(), name='ordered_view_detail'),
    path('order/status/<int:pk>/', UpdateOrderedStatus.as_view(), name='ordered_status'),
]


# from django.urls import path
# from .views import UserProfile, ListProduct, AddProducts, Productupdate, OrderProduct, OderedView, CartView

# urlpatterns = [
#     path('profile/', UserProfile.as_view(), name='user_profile'),
#     path('products/', ListProduct.as_view(), name='list_products'),
#     path('add-products/', AddProducts.as_view(), name='add_products'),
#     path('update-product/', Productupdate.as_view(), name='update_product'),
#     path('order-product/', OrderProduct.as_view(), name='order_product'),
#     path('view-orders/', OderedView.as_view(), name='view_orders'),
#     path('add-to-cart/', CartView.as_view(), name='add_to_cart'),
#     path('view-cart/', CartView.as_view(), name='view_cart'),
# ]