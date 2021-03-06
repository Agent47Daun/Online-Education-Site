from django.db import models
from user.models import TeacherAccount, StudentAccount

# Create your models here.


class Classroom(models.Model):
    teacher = models.ForeignKey(TeacherAccount,
                                on_delete=models.CASCADE,
                                related_name="classrooms")
    students = models.ManyToManyField(StudentAccount,
                                      related_name="classrooms")
    name = models.TextField(max_length=50)


class Lesson(models.Model):
    classroom = models.ForeignKey(Classroom,
                                  on_delete=models.CASCADE,
                                  related_name="lessons")
    oral_part = models.TextField(max_length=5000)
    name = models.TextField(max_length=100)


class Task(models.Model):
    lesson = models.ForeignKey(Lesson,
                               on_delete=models.CASCADE,
                               related_name="tasks")
    text = models.TextField(max_length=250)


class Answer(models.Model):
    task = models.ForeignKey(Task,
                             on_delete=models.CASCADE,
                             related_name="answers",
                             null=False, blank=False)
    text = models.TextField(max_length=250, null=False, blank=False)
    is_correct = models.BooleanField(default=False)
