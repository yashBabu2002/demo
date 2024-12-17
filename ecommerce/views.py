from django.shortcuts import render

# Create your views here.

from django.views import View
from django.http import JsonResponse, HttpResponse
from .models import User, Products, Cart, Order
from django.contrib.auth import get_user_model
from django.views.generic import UpdateView, ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .validations import validate


class ListProduct(ListView):
    def get(self, request, *args, **kwargs):
        products = Products.objects.all()
        data = [{
            "product_id":product.id,
            "name":product.name,
            "description":product.description,
            "stock":product.stock_quantity,
            "price":product.price
        }
        for product in products]

        return JsonResponse(data, safe=False, status=200)


@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AddProducts(View):
    def post(self, request):
        print(request.POST.get('name'))
        name = request.POST.get('name')
        description = request.POST.get('description')
        stock_quantity = request.POST.get('stock_quantity')
        price = request.POST.get('price')
        image = request.FILES.get('image')

        product = Products.objects.create(
            name=name,
            description=description,
            stock_quantity=stock_quantity,
            price=price,
            image=image
        )
    

        return JsonResponse({'message':'product added...'}, status=201)
    

@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class Productupdate(UpdateView):
    def post(self, request, *args, **kwargs):
        product_name = request.POST.get('product_name')
        stock = request.POST.get('stock')

        product = Products.objects.get(name=product_name)
        product.stock_quantity += int(stock)
        product.save()

        return JsonResponse({"message" :"product stock updated successfully"}, status=201)
    

@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class OrderProduct(View):
    def post(self, request):

        user = request.user
        product_name = request.POST.get('product_name')
        quantity = request.POST.get('quantity', 1)
        status = request.POST.get('status', 'pending')
        
        quantity = int(quantity)

        print("incomming product:", product_name)

        
        product = Products.objects.get(name=product_name)
        if product:
            print("product:", product)
        else:
            print("product error <<>>")
        
        print(product.name, product.stock_quantity)
        print(product.price)
        
        if  product.stock_quantity <= 0:
            return JsonResponse({"error":"Currently unavailable"})
        
        if quantity > product.stock_quantity:
            return JsonResponse({"error":f"cannot be purchased. only {product.stock_quantity} is available "})
        else:
            product.stock_quantity -= quantity

        total_price = product.price * quantity
        product.save()
        
        print("total_price:", total_price)

        print("user:",user)
        print("order_name:",product.name)
        print("order_quanity", quantity)
        print("total_price:", total_price)
        
        Order.objects.create(
        user=user,
        product=product,
        quantity=quantity,
        total_price=total_price,
        status=status
        )
        
        return JsonResponse({"message":"orded success"}, status=200)


@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class OderedView(View):
    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        data = [{
            "id":order.id,
            "product":order.product.name,
            "quantity":order.quantity,
            "price":order.total_price,
            "status":order.status
        }for order in orders]

        return JsonResponse(data, safe=False, status=200)
    

    def post(self, request, pk):

        order = get_object_or_404(Order, id=pk)
        status = request.POST.get('status')

        valid_status = [choice[0] for choice in order.STATUS_CHOICES]
        print(valid_status)
        print("order.status:",order.status)

        check_status = validate(status=status, ordered_status=order.status)
        if check_status:
            return check_status
        else:
            print("NO")

        if status in valid_status:
            order.status = status
            order.save()
            return JsonResponse({"message": f"Your order has been {status}"})
        return JsonResponse({"error":"Invaid status choice"})


@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class CartView(View):
    def get(self, request):
        print(request.user)
        
        carts = Cart.objects.filter(user=request.user)
        data = [{
            "user":cart.user.username,
            "product":cart.product.name,
            "quantity":cart.quantity,
            "price":cart.price

        }for cart in carts]

        return JsonResponse(data, safe=False, status=200)
    
    def post(self, request):
        user = request.user
        product_name = request.POST['product_name']
        quantity = request.POST.get('quantity', 1)
        

        product = get_object_or_404(Products, name=product_name)

        Cart.objects.create(
            user=user,
            product=product,
            quantity=quantity,
            price=product.price
        )
        return JsonResponse({"messgae":"product added to craft successfully"}, status=201)

