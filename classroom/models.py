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
                                  related_name="lessons")
    oral_part = models.TextField(max_length=5000)


class Task(models.Model):
    lesson = models.ForeignKey(Lesson,
                               on_delete=models.CASCADE,
                               related_name="tasks")
    text = models.TextField(max_length=250)

class Answer(models.Model):
    task = models.ForeignKey(Task,
                             on_delete=models.CASCADE,
                             related_name="answers")
    text = models.TextField(max_length=250)
    is_correct = models.BooleanField(default=False)