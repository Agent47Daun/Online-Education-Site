from django.urls import reverse
from rest_framework.test import APITestCase

from user.models import User


class ClassroomApiTest(APITestCase):
    url = reverse('classroom_list_create')

    def setUp(self):
        self.username_teacher = "test_username_teacher"
        self.password_teacher = "test_password"
        self.email_teacher = "test_user_teacher@test.com"
        self.user_teacher = User.objects.create_user(username=self.username_teacher, password=self.password_teacher, email=self.email_teacher, account_type=1)

        self.username_student = "test_username_student"
        self.password_student = "test_password"
        self.email_student = "test_user_student@test.com"
        self.user_student = User.objects.create_user(username=self.username_student, password=self.password_student, email=self.email_student)

    def test_classroom_list_as_teacher(self):
        self.client.force_login(self.user_teacher)

        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

    def test_classroom_list_as_student(self):
        self.client.force_login(self.user_student)

        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

    def test_classroom_create_as_student(self):
        self.client.force_login(self.user_student)

        response = self.client.post(self.url, {"name": "test_classroom", "teacher": self.user_teacher.teacher_account.id, "students": [self.user_student.student_account.id]})
        self.assertEqual(400, response.status_code)

    def test_classroom_create_as_teacher(self):
        self.client.force_login(self.user_teacher)

        response = self.client.post(self.url, {"name": "test_classroom", "teacher": self.user_teacher.teacher_account.id, "students": [self.user_student.student_account.id]})
        self.assertEqual(201, response.status_code)