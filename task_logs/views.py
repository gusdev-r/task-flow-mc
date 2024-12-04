from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import TaskLogSerializer
from _manager.utils import generate_hateoas_links, response_app
from rest_framework.views import status
from task.models import Task
from .models import TaskLog
import datetime


class TaskLogListView(APIView): ...


class TaskLogDetailView(APIView): ...


class TaskLogRecordProgressView(generics.CreateAPIView):
    serializer_class = TaskLogSerializer

    def post(self):
        try:
            ...
        except Exception as exc:
            return response_app(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                exception=True,
                data=str(exc),
            )


class TaskLogProgressView(APIView):
    def post(self, request, task_id):
        try:
            task = get_object_or_404(Task, id=task_id)
            serializer = TaskLogSerializer(data=request)
            serializer.is_valid(raise_exception=True)
            TaskLog.objects.create(
                task=task,
                log_message=serializer.validated_data["log_message"],
                log_level=serializer.validated_data["log_level"],
                timestamp=serializer.validated_data.get("timestamp", datetime.now()),
            )
            links = generate_hateoas_links(
                request=request,
                resource_name="task_log",
                obj_id=task.id,
                request_type="post",
            )
            return response_app(
                status_code=status.HTTP_201_CREATED,
                data="Log recorded successfully.",
                obj=serializer.data,
                links=links,
            )
        except Exception as exc:
            return response_app(
                status_code=status.HTTP_400_BAD_REQUEST,
                exception=True,
                data=str(serializer.errors),
            )
