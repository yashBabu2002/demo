from django.test import TestCase, Client

from .models import Products, Cart, Order, User
from django.urls import reverse
import json

class UserProfileTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345', email='test@example.com')
        self.client.login(username='testuser', password='12345')

    def test_get_user_profile(self):
        response = self.client.get(reverse('user_profile'))
        self.assertEqual(response.status_code, 302)
        self.assertContains(response, 'testuser')

    def test_update_user_profile(self):
        response = self.client.post(reverse('user_profile'), {
            'phone': '1234567890',
            'address': '123 Test St',
            'another_number': '0987654321'
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.phone, '1234567890')


class ProductTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.product = Products.objects.create(name='Test Product', description='A test product', stock_quantity=10, price=20.00)

    def test_list_products(self):
        response = self.client.get(reverse('list_products'))
        self.assertEqual(response.status_code, 302)
        self.assertContains(response, 'Test Product')

    def test_add_product(self):
        response = self.client.post(reverse('add_products'), {
            'name': 'New Product',
            'description': 'New Description',
            'stock_quantity': 5,
            'price': 15.00
        })
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Products.objects.filter(name='New Product').exists())


class OrderTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.product = Products.objects.create(name='Test Product', description='A test product', stock_quantity=10, price=20.00)

    def test_order_product(self):
        response = self.client.post(reverse('order_product'), {
            'product_name': 'Test Product',
            'quantity': 2
        })
        self.assertEqual(response.status_code, 200)
        order = Order.objects.first()
        self.assertEqual(order.quantity, 2)
        self.assertEqual(order.total_price, 40.00)

    def test_view_orders(self):
        Order.objects.create(user=self.user, product=self.product, quantity=1, total_price=20.00, status='pending')
        response = self.client.get(reverse('view_orders'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')


class CartTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.product = Products.objects.create(name='Test Product', description='A test product', stock_quantity=10, price=20.00)

    def test_add_to_cart(self):
        response = self.client.post(reverse('add_to_cart'), {
            'product_name': 'Test Product',
            'quantity': 1
        })
        self.assertEqual(response.status_code, 201)
        cart_item = Cart.objects.first()
        self.assertEqual(cart_item.product.name, 'Test Product')

    def test_view_cart(self):
        Cart.objects.create(user=self.user, product=self.product, quantity=1, price=20.00)
        response = self.client.get(reverse('view_cart'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')