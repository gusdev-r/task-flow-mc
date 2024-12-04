from django.shortcuts import get_object_or_404, render
from rest_framework import generics
from .serializers import TaskConfigSerializer, TaskSerializer, TaskUpdateSerializer
from .models import Task, TaskConfig, Status
from rest_framework.views import status
from _manager.utils import generate_hateoas_links, response_app
from rest_framework.views import APIView


class TaskListView(APIView):
    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        links = generate_hateoas_links(
            request=request, resource_name="task", obj_id=None, request_type="get"
        )

        return response_app(
            data="List of tasks retrieved successfully",
            obj=serializer.data,
            links=links,
        )


class TaskListByStatusView(APIView):
    def get(self, request):
        status_filter = request.query_params.get("status", None)
        if status_filter not in Status.values:
            return response_app(
                data=f"Invalid status '{status_filter}'. Allowed values: {', '.join(Status.values)}",
                obj=[],
                status=status.HTTP_400_BAD_REQUEST,
            )
        tasks = Task.objects.filter(status=status_filter)
        serializer = TaskSerializer(tasks, many=True)
        links = generate_hateoas_links(
            request=request, resource_name="task", request_type="get"
        )
        return response_app(
            data=f"List of {status_filter} tasks retrieved successfully",
            obj=serializer.data,
            links=links,
        )


class TaskDetailView(APIView):
    def get(self, request, task_id, *args, **kwargs):
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return response_app(
                status_code=status.HTTP_404_NOT_FOUND,
                exception=True,
                data="Task not found",
            )

        serializer = TaskSerializer(task)
        links = generate_hateoas_links(
            request=request, resource_name="task", obj_id=task_id, request_type="get"
        )

        return response_app(
            data="Task details retrieved successfully",
            obj=serializer.data,
            links=links,
        )


class TaskCreateView(generics.CreateAPIView):
    serializer_class = TaskSerializer

    def post(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            links = generate_hateoas_links(
                request=request,
                resource_name="task",
                obj_id=serializer.data.get("id"),
                request_type="post",
            )
            return response_app(
                status_code=status.HTTP_201_CREATED,
                data="Task created successfully!",
                obj=serializer.data,
                links=links,
            )
        except Exception as exc:
            return response_app(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                exception=True,
                data=str(exc),
            )


class TaskDeleteView(APIView):
    def delete(self, request, task_id, *args, **kwargs):
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return response_app(
                "Task not found", status_code=status.HTTP_404_NOT_FOUND, exception=True
            )
        task.delete()
        links = generate_hateoas_links(
            request=request,
            resource_name="task",
            obj_id=task_id,
            request_type="delete",
        )

        return response_app(
            status_code=status.HTTP_204_NO_CONTENT,
            data="Task deleted successfully",
            links=links,
        )


class TaskUpdateView(APIView):
    def put(self, request, task_id, *args, **kwargs):
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return response_app(
                "Task not found", status_code=status.HTTP_404_NOT_FOUND, exception=True
            )
        serializer = TaskUpdateSerializer(task, data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            task = serializer.save()
            links = generate_hateoas_links(
                request=request,
                resource_name="task",
                obj_id=task.id,
                request_type="put",
            )

            return response_app(
                status_code=status.HTTP_201_CREATED,
                data="Task updated successfully",
                obj=serializer.data,
                links=links,
            )
        except Exception as exc:
            return response_app(
                status_code=status.HTTP_400_BAD_REQUEST, exception=True, data=str(exc)
            )


class TaskConfigList(APIView):
    def get(self, request):
        tasks_config = TaskConfig.objects.all()
        serializer = TaskConfigSerializer(tasks_config, many=True)
        links = generate_hateoas_links(
            request=request, resource_name="task", obj_id=None, request_type="get"
        )

        return response_app(
            data="List of tasks configs retrieved successfully",
            obj=serializer.data,
            links=links,
        )


class TaskConfigDeleteView(APIView):
    def delete(self, request, task_id, *args, **kwargs):
        try:
            task_config = TaskConfig.objects.get(id=task_id)
        except Task.DoesNotExist:
            return response_app(
                "Task config not found",
                status_code=status.HTTP_404_NOT_FOUND,
                exception=True,
            )
        task_config.delete()
        links = generate_hateoas_links(
            request=request,
            resource_name="task",
            obj_id=task_id,
            request_type="delete",
        )

        return response_app(
            status_code=status.HTTP_204_NO_CONTENT,
            data="Task config deleted successfully",
            links=links,
        )


class TaskConfigCreateView(generics.CreateAPIView):
    serializer_class = TaskConfigSerializer

    def post(self, request, *args, **kwargs):
        try:
            task_id = self.kwargs.get("task_id")
            task = get_object_or_404(Task, id=task_id)

            mutable_data = request.data.copy()
            mutable_data["task"] = task.id
            serializer = self.get_serializer(data=mutable_data)
            serializer.is_valid(raise_exception=True)
            config, created = TaskConfig.objects.update_or_create(
                task=task, defaults=serializer.validated_data
            )
            status_message = "created" if created else "updated"
            links = generate_hateoas_links(
                request=request,
                resource_name="task",
                obj_id=task.id,
                request_type="post",
            )

            return response_app(
                status_code=status.HTTP_201_CREATED,
                data=f"Task configuration {status_message} successfully.",
                obj=serializer.data,
                links=links,
            )
        except Exception as exc:
            return response_app(
                status_code=status.HTTP_400_BAD_REQUEST,
                exception=True,
                data=str(exc),
            )
