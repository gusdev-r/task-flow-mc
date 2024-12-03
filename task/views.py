from django.shortcuts import render
from rest_framework import generics
from .serializers import TaskSerializer, TaskUpdateSerializer
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
