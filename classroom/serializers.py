from rest_framework import serializers

from classroom.models import Classroom, Lesson, Task, Answer
from user.serializers import TeacherSerializer, StudentSerializer, TeacherDetailSerializer, StudentDetailSerializer
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


class ClassroomRetrieveUpdateDestorySerializer(serializers.ModelSerializer):

    students = StudentDetailSerializer(many=True, read_only=True)
    teacher = TeacherDetailSerializer(read_only=True)

    class Meta:
        model = Classroom
        fields = "__all__"


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ['text', 'is_correct',]

        extra_kwargs = {
            "is_correct": {
                "required": True
            }
        }


class TaskSerializer(serializers.ModelSerializer):

    answers = AnswerSerializer(many=True)

    class Meta:
        model = Task
        fields = ['text', "answers"]


class LessonSerializer(serializers.ModelSerializer):

    tasks = TaskSerializer(many=True)

    class Meta:
        model = Lesson
        fields = ['oral_part', 'name', 'tasks']

    def create(self, validated_data):
        classroom_id = self.context['classroom_id']
        classroom = Classroom.objects.get(id=classroom_id)
        lesson = Lesson.objects.create(classroom=classroom, name=validated_data['name'], oral_part=validated_data['oral_part'])

        for task in validated_data['tasks']:
            task_instance = Task.objects.create(text=task['text'], lesson=lesson)
            answers = []
            for answer in task['answers']:
                answers.append(Answer.objects.create(text=answer['text'], is_correct=answer['is_correct'], task=task_instance))
            task_instance.save()

        return lesson

    def validate(self, validated_data):      
        classroom_id = self.context.get("classroom_id")
        if not Classroom.objects.filter(id=classroom_id).exists():
            raise serializers.ValidationError({"detail": "Не найден класс с таким ID."}, 400)

        return validated_data
