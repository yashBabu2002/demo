from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

class UserProfileTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        self.client.login(username='testuser', password='password123')

    def test_get_user_profile(self):
        response = self.client.get(reverse('user_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('username', response.json()['data'])

    def test_update_user_profile(self):
        data = {
            'phone': '1234567890',
            'address': 'New Address',
            'another_number': '0987654321'
        }
        response = self.client.post(reverse('user_profile'), data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'user profile updated')
