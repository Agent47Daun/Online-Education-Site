from django.urls import reverse

from rest_framework.test import APITestCase

from .models import User


class UserRegistrationTest(APITestCase):
    url = reverse("user-list")

    def test_valid_data(self):
        user_data = {
            "username": "test_username",
            "password": "test_password",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "email": "test_user@test.com"
        }

        response = self.client.post(self.url, user_data)
        self.assertEqual(201, response.status_code)

    def test_unique_username_email(self):
        user_data = {
            "username": "test_username",
            "password": "test_password",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "email": "test_user@test.com"
        }
        response = self.client.post(self.url, user_data)
        self.assertEqual(201, response.status_code)

        #  Username unique test
        second_user_data = {
            "username": "test_username",
            "password": "test_password",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "email": "test_user@test.com123"
        }
        response = self.client.post(self.url, second_user_data)
        self.assertEqual(400, response.status_code)

        #  Email unique test
        third_user_data = {
            "username": "test_username123",
            "password": "test_password",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "email": "test_user@test.com"
        }
        response = self.client.post(self.url, third_user_data)
        self.assertEqual(400, response.status_code)


class UserLoginTest(APITestCase):
    url = reverse("knox_login")
    token_test_url = reverse('user-me')

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
        self.assertTrue(response.data.get("token"))

        #  Token test
        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        test_token_response = self.client.get(self.token_test_url)
        self.assertEqual(200, test_token_response.status_code)


class UserRetrieveUpdateTest(APITestCase):
    url = reverse("user-me")

    def setUp(self):
        self.username = "test_username"
        self.password = "test_password"
        self.email = "test_user@test.com"
        self.user = User.objects.create_user(username=self.username, password=self.password, email=self.email)

    def test_unauthorized_retrieve(self):
        response = self.client.get(self.url)
        self.assertEqual(401, response.status_code)

    def test_authorized_retrieve(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.username, response.data['username'])