from rest_framework import generics, viewsets
from rest_framework.response import Response


from classroom.models import Classroom
from classroom.serializers import ClassroomCreateListSerializer


class ClassroomCreateListApiView(generics.ListCreateAPIView):
    serializer_class = ClassroomCreateListSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_teacher:
            queryset = Classroom.objects.filter(teacher__id=user.teacher_account.id)
        else:
            queryset = Classroom.objects.filter(students__id=user.student_account.id)

        return queryset
