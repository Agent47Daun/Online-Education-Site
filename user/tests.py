from django.urls import reverse

from rest_framework.test import APITestCase

from .models import User

class UserRegistrationTest(APITestCase):
    url = reverse("user-list")

    def test_valid_data(self):

        user_data = {
            "username": "test_username",
            "password": "test_password",
            "email": "test_user@test.com"
        }

        response = self.client.post(self.url, user_data)
        self.assertEqual(201, response.status_code)

    def test_unique_username_email(self):

        user_data = {
            "username": "test_username",
            "password": "test_password",
            "email": "test_user@test.com"
        }
        response = self.client.post(self.url, user_data)
        self.assertEqual(201, response.status_code)

        #  Username unique test
        second_user_data = {
            "username": "test_username",
            "password": "test_password",
            "email": "test_user@test.com123"
        }
        response = self.client.post(self.url, second_user_data)
        self.assertEqual(400, response.status_code)

        #  Email unique test
        third_user_data = {
            "username": "test_username123",
            "password": "test_password",
            "email": "test_user@test.com"
        }
        response = self.client.post(self.url, third_user_data)
        self.assertEqual(400, response.status_code)


class UserLoginTest(APITestCase):
    url = reverse("knox_login")

    def setUp(self):
        self.username = "test_username"
        self.password = "test_password"
        self.email = "test_user@test.com"
        self.user = User.objects.create_user(username=self.username, password=self.password, email=self.email)

    def test_without_password(self):
        response = self.client.post(self.url, {"username": self.username})
        self.assertEqual(400, response.status_code)

    def test_wrong_password(self):
        response = self.client.post(self.url, {"username": self.username, "password": "-1"})
        self.assertEqual(400, response.status_code)

    def test_valid_data(self):
        response = self.client.post(self.url, {"username": self.username, "password": self.password})
        self.assertEqual(200, response.status_code)
