from rest_framework import generics, viewsets

from .models import Classroom, Lesson, Task, Answer
from .serializers import ClassroomSerializer

class ClassroomApiView(viewsets.ModelViewSet):

    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer