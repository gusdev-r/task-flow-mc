from django.db import models
import uuid
from task.models import Task


class Log_type(models.TextChoices):
    INFO = "Info"
    WARNING = "Warning"
    ERROR = "Error"


class TaskLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task = models.ForeignKey(Task)
    log_message = models.TextField()
    log_level = models.CharField(max_length=50, choices=Log_type.choices)
    timestamp = models.DateTimeField()
