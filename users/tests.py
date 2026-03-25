from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User

class UsersTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_registration(self):
        response = self.client.post("/users/register/", {
            "username": "newuser",
            "password": "strongpassword"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_user_login(self):
        User.objects.create_user(username="loginuser", password="123456")
        response = self.client.post("/users/login/", {
            "username": "loginuser",
            "password": "123456"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
