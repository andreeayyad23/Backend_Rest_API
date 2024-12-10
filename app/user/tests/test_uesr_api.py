from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

# Define URLs for API endpoints
CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    """Helper function to create a user"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating a user with valid payload is successful"""
        payload = {
            'email': 'test@example.com',  # Corrected email format
            'password': 'test123',       # Valid password
            'name': 'Test Name'          # Valid name
        }
        res = self.client.post(CREATE_USER_URL, payload)

        # Debugging: Print response if the test fails
        if res.status_code != status.HTTP_201_CREATED:
            print(f"Response Data: {res.data}")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating a user that already exists fails"""
        payload = {
            'email': 'test@example.com',
            'password': 'test123',
            'name': 'Test Name'
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that a password must be more than 5 characters"""
        payload = {
            'email': 'test@example.com',
            'password': 'pw',  # Invalid password
            'name': 'Test Name'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        # Debugging: Print response if the test fails
        if res.status_code != status.HTTP_400_BAD_REQUEST:
            print(f"Response Data: {res.data}")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        payload = {
            'email': 'test@example.com',
            'password': 'test123'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        # Debugging: Print response if the test fails
        if res.status_code != status.HTTP_200_OK:
            print(f"Response Data: {res.data}")

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        create_user(email='test@example.com', password='test123')
        payload = {
            'email': 'test@example.com',
            'password': 'wrong'
        }
        res = self.client.post(TOKEN_URL, payload)

        # Debugging: Print response if the test fails
        if res.status_code != status.HTTP_400_BAD_REQUEST:
            print(f"Response Data: {res.data}")

        self.assertNotIn('token', res.data)  
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)  

    def test_create_token_no_user(self):
        """Test that token is not created if user doesn't exist"""
        payload = {
            'email': 'test@example.com',
            'password': 'test123'
        }
        res = self.client.post(TOKEN_URL, payload)

        # Debugging: Print response if the test fails
        if res.status_code != status.HTTP_400_BAD_REQUEST:
            print(f"Response Data: {res.data}")  

        self.assertNotIn('token', res.data)  
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})

        # Debugging: Print response if the test fails
        if res.status_code != status.HTTP_400_BAD_REQUEST:
            print(f"Response Data: {res.data}")  

        self.assertNotIn('token', res.data)  
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)  