from rest_framework import serializers

from .models import User, StudentAccount, TeacherAccount

class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = TeacherAccount
        fields = ['classrooms', 'user']


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentAccount
        fields = ['classrooms', 'user']


class UserSerializer(serializers.ModelSerializer):

    teacher_account = TeacherSerializer(read_only=True)
    student_account = StudentSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', "student_account", "teacher_account"]