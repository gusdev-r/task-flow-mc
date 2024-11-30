from rest_framework import serializers
from .models import Task, TaskConfig
from rest_framework.reverse import reverse


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    self_url = serializers.HyperlinkedIdentityField(
        view_name="task-detail", lookup_field="id"
    )

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
        ]


def to_representation(self, instance):
    representation = super().to_representation(instance)
    representation["update"] = reverse(
        "task-update", kwargs={"id": instance.id}, request=self.context.get("request")
    )
    representation["delete"] = reverse(
        "task-delete", kwargs={"id": instance.id}, request=self.context.get("request")
    )
    return representation


class TaskConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskConfig
        fields = ["id", "task", "config_key", "config_value"]
