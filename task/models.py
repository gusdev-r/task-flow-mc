from django.db import models
from user.models import User
import uuid


class Status(models.TextChoices):
    PENDING = "Pending"
    RUNNING = "Running"
    FAILURE = "Failure"
    CONCLUDED = "Concluded"


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300, blank=False)
    status = models.CharField(max_length=50, choices=Status.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    result = models.JSONField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="task")


class TaskConfig(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="task")
    config_key = models.CharField(max_length=50)
    config_value = models.JSONField()
