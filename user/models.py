from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
# Create your models here.


class StudentAccount(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='student_account',
                                blank=True,
                                null=True)

    def __str__(self):
        return "Student:{} {}".format(self.user.username, self.id)


class TeacherAccount(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='teacher_account',
                                blank=True,
                                null=True)

    def __str__(self):
        return "Teacher: {} {}".format(self.user.username, self.id)


class User(AbstractUser):
    STUDENT = 0
    TEACHER = 1
    account_type_choices = (
        (STUDENT, "Student"),
        (TEACHER, "Teacher")
    )

    REQUIRED_FIELDS = ["email", "account_type", "first_name", "last_name"]

    username = models.CharField(max_length=150, null=False, blank=False, unique=True)

    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    account_type = models.IntegerField(choices=account_type_choices, default=STUDENT)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return "{}: {}".format(self.username, self.id)