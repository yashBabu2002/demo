from django.views import View
from django.http import JsonResponse, HttpResponse
from django.views.generic import UpdateView, ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

from .models import Product, Cart, Order
from .validations import validate, validate_product
from django.core.paginator import Paginator
import json

@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class UserProfile(View):
    def get(self, request):
        user = request.user
        data = {
            'user_id':user.id,
            'username':user.username,
            'email':user.email,
            'phone':int(str(user.phone)),
            'address':user.address,
            'another_number':str(user.another_number)
        }
        return JsonResponse({'success':True, 'data':data}, status=200)

    def post(self, request):

        user = request.user
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'success':False, 'error':'Invaid Json'}, status=400)
        
        phone = data.get('phone', user.phone)
        another_number = data.get('another_number', user.another_number)
        address = data.get('address', user.address)

        if not phone or not address or not another_number:
            return JsonResponse({'success':False, 'error':'All fields are required'}, status=400)

        user.phone = phone
        user.address = address
        user.another_number = another_number
        user.save()

        return JsonResponse({'success':True, 'message':'user profile updated'}, status=200)
        


class ListProduct(ListView):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()

        page_number = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 5)
        paginator = Paginator(products, page_size)
        page = paginator.get_page(page_number)

        data = [{
            'product_id':product.id,
            'name':product.name,
            'description':product.description,
            'stock':product.stock_quantity,
            'price':product.price
        }
        for product in page]

        response_data = {
            'success': True,
            'data': data,
            'pagination': {
                'total_items': paginator.count,
                'total_pages': paginator.num_pages,
                'current_page': page.number,
                'page_size': page_size,
                'has_next': page.has_next(),
                'has_previous': page.has_previous()
            }
        }

        return JsonResponse(response_data, status=200)


@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AddProducts(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'success':False, 'error':'Invalid Json'}, status=400)
        
        name = data.get('name')
        description = data.get('description')
        stock_quantity = data.get('stock_quantity')
        price = data.get('price')
        image = request.FILES.get('image')

        check_product = validate_product(name=name,
                                         description=description,
                                         stock_quantity=stock_quantity,
                                         price=price
                                         )
        if check_product:
            return check_product
        
        product = Product.objects.create(
            name=name,
            description=description,
            stock_quantity=stock_quantity,
            price=price,
            image=image
        )
    

        return JsonResponse({'message':'product created successfully'}, status=201)
    

@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class Productupdate(UpdateView):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'success':False, 'error':'Invalid Json'}, status=400)
        
        product_name = data.get('product_name')
        
        try:
            product = Product.objects.get(name=product_name)
        except Product.DoesNotExist:
            return JsonResponse({'success':False, 'error':'Product not found'}, status=404)
        
        update_fields = []

        
        if 'stock_quantity' in data:
            product.stock_quantity += int(data.get('stock_quantity'))
            update_fields.append('stock_quantity')

        
        if 'description' in data:
            product.description = data.get('description')
            update_fields.append('description')
        
        if 'price' in data:
            product.price = data.get('price')
            update_fields.append('price')

        if update_fields:
            product.save()  
            return JsonResponse({'success':True, 'message' :'Product updated successfully'}, status=200)
        return JsonResponse({'success':False, 'error':'No valid fields to update the product'})
        
    

@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class OrderProduct(View):
    def post(self, request):

        user = request.user
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'success':False, 'error':'Invalid Json'}, status=400)
        product_name = data.get('product_name')
        quantity = int(data.get('quantity', 1)) 
        status = data.get('status', 'pending')
        

        if not product_name or quantity <=0:
            return JsonResponse({'success':False, 'error':'Invalid product_name or quantity'}, status=400)
        
        try: 
            product = Product.objects.get(name=product_name)
        except Product.DoesNotExist:
            return JsonResponse({'success':False, 'error':'Product not found'}, status=404)
        
        if product.stock_quantity <= 0:
            return JsonResponse({'error':'Currently unavailable'}, status=400)
        
        if quantity > product.stock_quantity:
            return JsonResponse({'error':f'cannot be purchased. only {product.stock_quantity} is available '}, status=400)

        product.stock_quantity -= quantity
        total_price = product.price * quantity
        print(total_price)
        product.save()
       
 
        Order.objects.create(
        user=user,
        product=product,
        quantity=quantity,
        total_price=total_price,
        status=status
        )
        
        return JsonResponse({'message':'Product Ordered Successfully'}, status=200)


@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class OderedView(View):
    def get(self, request, pk=None):
        if pk:
            orders = Order.objects.filter(user=request.user, id=pk)
            data = [{
                'id':order.id,
                'product':order.product.name,
                'quantity':order.quantity,
                'price':order.total_price,
                'status':order.status
            }for order in orders]

            return JsonResponse(data, safe=False, status=200)
        
        else:
            orders = Order.objects.filter(user=request.user)
            data = [{
                'id':order.id,
                'product':order.product.name,
                'quantity':order.quantity,
                'price':order.total_price,
                'status':order.status
            }for order in orders]

            return JsonResponse(data, safe=False, status=200)

@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')  
class UpdateOrderedStatus(View):
    def post(self, request, pk):

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'success':False, 'error':'Invalid Json'}, status=400)

        status = data.get('status')

        order = get_object_or_404(Order, id=pk)
        valid_status = [choice[0] for choice in order.STATUS_CHOICES]
      
        check_status = validate(status=status, ordered_status=order.status)
        if check_status:
            return check_status
       
        if status in valid_status:
            order.status = status
            order.save()
            return JsonResponse({'message': f'Your order has been {status}'}, status=201)
        return JsonResponse({'error':'Invaid status choice'}, status=400)


@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class CartView(View):
    def get(self, request, pk=None):
        print(pk)

        if pk:
            carts = Cart.objects.filter(user=request.user, id=pk)
            data = [{
                # 'user':cart.user.username,
                'id':cart.id,
                'product':cart.product.name,
                'quantity':cart.quantity,
                'price':cart.price

            }for cart in carts]

            return JsonResponse(data, safe=False, status=200)
        
        
        else:
            carts = Cart.objects.filter(user=request.user)
            data = [{
                # 'user':cart.user.username,
                'id':cart.id,
                'product':cart.product.name,
                'quantity':cart.quantity,
                'price':cart.price

            }for cart in carts]

            return JsonResponse(data, safe=False, status=200)
    
    def post(self, request):
        user = request.user
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'success':False, 'error':'Invalid Json'}, status=400)
        
        product_name = data.get('product_name')
        quantity = int(data.get('quantity', 1))
        
        if not product_name or quantity <= 0:
            return JsonResponse({'error':'Invalid product name or quantity'}, status=400)

        product = get_object_or_404(Product, name=product_name)
        print(product.price)

        Cart.objects.create(
            user=user,
            product=product,
            quantity=quantity,
            price=product.price
        )
        return JsonResponse({'messgae':'product added to craft successfully'}, status=201)

