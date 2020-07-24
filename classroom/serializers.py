from rest_framework import serializers

from classroom.models import Classroom
from user.serializers import TeacherSerializer, StudentSerializer
from user.models import StudentAccount, TeacherAccount


class ClassroomCreateListSerializer(serializers.ModelSerializer):
    students = serializers.PrimaryKeyRelatedField(many=True, queryset=StudentAccount.objects.all())
    teacher = serializers.PrimaryKeyRelatedField(queryset=TeacherAccount.objects.all())

    class Meta:
        model = Classroom
        fields = ['name', 'teacher', 'students']

    def create(self, validated_data):

        if self.context['request'].user.is_teacher:
            return super().create(validated_data)
        else:
            raise serializers.ValidationError({"detail": "Класс может быть создан только учителем."})
