from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import CustomUser

class RegistrationTestCase(APITestCase):

    def test_registration(self):
        data = {
            "email": "testuser@test.com",
            "username": "testuser",
            "password": "strong_password_123",
            "name": "Test User"
        }
        response = self.client.post(reverse('name-of-registration-view'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)
