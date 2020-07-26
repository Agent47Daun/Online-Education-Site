import copy

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
        fields = ['id', 'text', 'is_correct',]

        extra_kwargs = {
            "is_correct": {
                "required": True
            }
        }


class TaskSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Task
        fields = ['id', 'text', "answers"]


class LessonAddSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True)

    class Meta:
        model = Lesson
        fields = ['id', 'oral_part', 'name', 'tasks', 'classroom']

        extra_kwargs = {
            "classroom": {
                "read_only": "True"
            }
        }

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

        lesson.save()

        return lesson

    def validate(self, validated_data):
        classroom_id = self.context.get("classroom_id")
        if not Classroom.objects.filter(id=classroom_id).exists():
            raise serializers.ValidationError({"detail": "Не найден класс с таким ID."}, 400)

        return validated_data


class LessonDetailSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True)

    class Meta:
        model = Lesson
        fields = ['id', 'oral_part', 'name', 'tasks', 'classroom']

        extra_kwargs = {
            "classroom": {
                "read_only": "True"
            },
        }

    def update(self, instance, validated_data):
        data = copy.deepcopy(validated_data)

        tasks_data = data['tasks']
        tasks = list(instance.tasks.all())

        if len(tasks) > len(tasks_data):
            raise serializers.ValidationError({"detail": "Переданных заданий меньше чем существует у данного урока."})

        instance.oral_part = data['oral_part']
        instance.name = data['name']

        for task_data in tasks_data:
            task = tasks.pop(0)
            task.text = task_data.get('text', task.text)

            answers_data = task_data.get('answers')
            answers = list(task.answers.all())

            if len(answers) > len(answers_data):
                raise serializers.ValidationError({"detail": "Переданных вариантов ответа меньше чем существует у данного задания."})

            for answer_data in answers_data:
                answer = answers.pop(0)
                answer.text = answer_data.get('text', answer.text)
                answer.is_correct = answer_data.get('is_correct', answer.is_correct)
                answer.save()

            task.save()
        instance.save()

        return instance

    def validate(self, validated_data):
        data = copy.deepcopy(validated_data)
        print(data)
        tasks_data = data.get('tasks')
        if not tasks_data:
            raise serializers.ValidationError({"tasks": "Заданий не может быть меньше 1."})

        for task_data in tasks_data:

            answers_data = task_data.get('answers')
            if not answers_data:
                raise serializers.ValidationError({"answers": "Вариантов ответов не может быть меньше 1."})

        return data
