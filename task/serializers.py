from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Task, TaskConfig


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


class TaskUpdateSerializer(ModelSerializer):
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


class TaskConfigSerializer(ModelSerializer):
    class Meta:
        model = TaskConfig
        fields = ["id", "task", "config_key", "config_value"]

    def validate(self, data):
        if data["config_key"] not in ["timeout", "priority"]:
            raise serializers.ValidationError("Invaliud configuration Key")

        if data["config_key"] == "timeout" and not (
            1 <= int(data["config_value"]) <= 3600
        ):
            raise serializers.ValidationError(
                "Timeout must bet between 1 and 3600 seconds."
            )

        return data
