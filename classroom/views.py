from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response


from classroom.models import Classroom, Lesson
from classroom.serializers import ClassroomCreateListSerializer, LessonSerializer, ClassroomRetrieveUpdateDestorySerializer


class ClassroomCreateListApiView(generics.ListCreateAPIView):
    serializer_class = ClassroomCreateListSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_teacher:
            queryset = Classroom.objects.filter(teacher__id=user.teacher_account.id)
        else:
            queryset = Classroom.objects.filter(students__id=user.student_account.id)

        return queryset


class ClassroomAddLesson(generics.CreateAPIView):
    serializer_class = LessonSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        uri = self.request.build_absolute_uri()
        classroom_id = uri.split("/")[-3]
        context.update({'classroom_id': classroom_id})
        return context


class ClassroomRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClassroomRetrieveUpdateDestorySerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_teacher:
            queryset = Classroom.objects.filter(teacher__id=user.teacher_account.id)
        else:
            queryset = Classroom.objects.filter(students__id=user.student_account.id)

        return queryset
