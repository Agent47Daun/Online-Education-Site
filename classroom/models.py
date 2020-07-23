from django.db import models
from user.models import TeacherAccount, StudentAccount

# Create your models here.


class Classroom(models.Model):
    teacher = models.ForeignKey(TeacherAccount,
                                on_delete=models.CASCADE,
                                related_name="classrooms")
    students = models.ManyToManyField(StudentAccount,
                                      related_name="classrooms")


class Lesson(models.Model):
    classroom = models.ForeignKey(Classroom,
                                  on_delete=models.CASCADE,
                                  related_name="lesson")
    oral_part = models.TextField(max_length=5000)