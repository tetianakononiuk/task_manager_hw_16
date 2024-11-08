from rest_framework import serializers
from my_app.models.task import SubTask, Category, Task
from rest_framework.exceptions import ValidationError
from django.utils import timezone


class TaskCreateSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'deadline', 'owner']

    def validate_deadline(self, value):
        if value < timezone.now():
            raise ValidationError('The deadline cannot be in the past.')
        return value


class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = serializers.SerializerMethodField()
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline', 'created_at', 'subtasks', 'owner']

    def get_subtasks(self, obj):
        return SubTaskSerializer(obj.subtasks.all(), many=True).data


class SubTaskCreateSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SubTask
        fields = ['title', 'description', 'task', 'deadline', 'status', 'owner']


class SubTaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = SubTask
        fields = ['id', 'title', 'description', 'status', 'deadline', 'created_at', 'owner']


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'description']

    def validate_name(self, value):
        if Category.objects.filter(name=value).exists():
            raise ValidationError('Category with this name already exists.')
        return value