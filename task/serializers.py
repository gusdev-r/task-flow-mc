from rest_framework.serializers import ModelSerializer

from notifications import serializers
from .models import Task, TaskConfig
from rest_framework.reverse import reverse


class TaskSerializer(ModelSerializer):

    class Meta:
        model = Task
        fields = [
            "id",
            "name",
            "description",
            "status",
            "result",
            "created_at",
            "updated_at",
            "user",
        ]


class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "name",
            "description",
            "status",
            "result",
            "user",
        ]
        extra_kwargs = {
            "name": {"required": False},
            "description": {"required": False},
            "status": {"required": False},
            "result": {"required": False},
            "user": {"required": False},
        }


class TaskConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskConfig
        fields = ["id", "task", "config_key", "config_value"]
