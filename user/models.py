from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
# Create your models here.


class StudentAccount(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='student_account')


class TeacherAccount(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='teacher_account')


class User(AbstractUser):

    email = models.EmailField(unique=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return "{}: {}".format(self.username, self.id)