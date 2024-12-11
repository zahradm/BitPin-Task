from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from app.users.models import User


class UserRegisterViewTestCase(APITestCase):
    def test_register_user(self):
        url = reverse('user-register')
        user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword123"
        }

        response = self.client.post(url, user_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertEqual(response.data["username"], user_data["username"])
        self.assertEqual(response.data["email"], user_data["email"])

        self.assertTrue(User.objects.filter(username=user_data["username"]).exists())

    def test_register_user_invalid_data(self):
        url = reverse('user-register')
        invalid_data = {
            "username": "",
            "email": "invalidemail",
            "password": ""
        }

        response = self.client.post(url, invalid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)
        self.assertIn("email", response.data)
        self.assertIn("password", response.data)


class SuperUserRegisterViewTestCase(APITestCase):
    def test_register_superuser(self):
        url = reverse('user-register-superuser')
        superuser_data = {
            "username": "adminuser",
            "email": "adminuser@example.com",
            "password": "adminpassword123"
        }

        response = self.client.post(url, superuser_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertEqual(response.data["username"], superuser_data["username"])
        self.assertEqual(response.data["email"], superuser_data["email"])

        user = User.objects.get(username=superuser_data["username"])
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_register_superuser_invalid_data(self):
        url = reverse('user-register-superuser')
        invalid_data = {
            "username": "",
            "email": "invalidemail",
            "password": ""
        }

        response = self.client.post(url, invalid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)
        self.assertIn("email", response.data)
        self.assertIn("password", response.data)
