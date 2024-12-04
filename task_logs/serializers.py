from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import TaskLog, Log_type


class TaskLogSerializer(ModelSerializer):
    class Meta:
        model = TaskLog
        fields = ["id", "task", "log_message", "timestamp"]
        extra_kwargs = {"timestamp": {"required": False}}

    def validate_log_level(self, value):
        if value not in Log_type.value:
            raise
