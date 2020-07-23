from rest_framework import serializers
from .models import Classroom, Lesson, Task, Answer


class ClassroomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Classroom