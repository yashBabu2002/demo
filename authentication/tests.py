from django.test import TestCase, Client
from django.urls import reverse
from ecommerce.models import User

class UserAuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')  # Adjust the name as per your URL configuration
        self.login_url = reverse('login')  # Adjust the name as per your URL configuration
        self.logout_url = reverse('logout')  # Adjust the name as per your URL configuration
        

    def test_register_success(self):
        response = self.client.post(self.register_url, {
            'username': 'testuser',
            'email': 'test@example.com',
            'phone': '1234567890',
            'another_number': '0987654321',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"message": "user created successfully"})
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_register_failure_due_to_password_mismatch(self):
        response = self.client.post(self.register_url, {
            'username': 'testuser',
            'email': 'test@example.com',
            'phone': '1234567890',
            'another_number': '0987654321',
            'password': 'password123',
            'confirm_password': 'differentpassword'
        })
        self.assertEqual(response.status_code, 400)  # Adjust based on your validation response
        self.assertIn("error", response.json())

    def test_login_success(self):
        # First, register a user
        self.client.post(self.register_url, {
            'username': 'testuser',
            'email': 'test@example.com',
            'phone': '1234567890',
            'another_number': '0987654321',
            'password': 'password123',
            'confirm_password': 'password123'
        })

        # Now, try to log in
        response = self.client.post(self.login_url, {
            'email': 'test@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "user logged in successfully"})


    def test_login_failure_due_to_invalid_credentials(self):
        response = self.client.post(self.login_url, {
            'email': 'nonexistent@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"error": "Invalid username and password"})


    def test_logout_success(self):
        # First, register and log in a user
        self.client.post(self.register_url, {
            'username': 'testuser',
            'email': 'test@example.com',
            'phone': '1234567890',
            'another_number': '0987654321',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        self.client.post(self.login_url, {
            'email': 'test@example.com',
            'password': 'password123'
        })

        # Now, log out
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "user logged out successfully"})

    def test_logout_failure_due_to_invalid_method(self):
        response = self.client.get(self.logout_url)  # Using GET instead of POST
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json(), {"error": "Invalid request method"})