from django.shortcuts import render
from rest_framework import generics
from .serializers import TaskSerializer
from .models import Task, TaskConfig
from rest_framework.views import status
from _manager.utils import generate_hateoas_links, response_app
from rest_framework.views import APIView


class TaskListAllView(APIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def get(self, request):
        tasks = self.get_queryset()
        serializer = self.get_serializer(tasks, many=True)
        links = generate_hateoas_links(request, "tasks", request_type="get")

        return response_app(
            data="List of tasks retrieved successfully",
            obj=serializer.data,
            links=links,
        )


class TaskDetailView(APIView):
    def get(self, request, id, *args, **kwargs):
        try:
            task = Task.objects.get(id=id)
        except Task.DoesNotExist:
            return response_app(
                status_code=status.HTTP_404_NOT_FOUND,
                exception=True,
                data="Task not found",
            )

        serializer = TaskSerializer(task)
        links = generate_hateoas_links(
            request=request, resource_name="tasks", id=task.id, request_type="get"
        )

        return response_app(
            data="Task details retrieved successfully",
            obj=serializer.data,
            links=links,
        )


class TaskCreateView(generics.CreateAPIView):
    serializer_class = TaskSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            links = generate_hateoas_links(
                request=request,
                resource_name="tasks",
                id=serializer.data.id,
                request_type="post",
            )
            return response_app(
                status_code=status.HTTP_201_CREATED,
                data="Task created successfully!",
                obj=serializer.data,
                links=links,
            )
        return response_app(
            status_code=status.HTTP_400_BAD_REQUEST, exception=True, data="Invalid data"
        )


class TaskDeleteView(APIView):
    def delete(self, request, id, *args, **kwargs):
        try:
            task = Task.objects.get(id=id)
        except Task.DoesNotExist:
            return response_app(
                "Task not found", status_code=status.HTTP_404_NOT_FOUND, exception=True
            )
        task.delete()
        links = generate_hateoas_links(request, "tasks", id, request_type="delete")

        return response_app(
            status_code=status.HTTP_204_NO_CONTENT,
            data="Task deleted successfully",
            links=links,
        )


class TaskUpdateView(APIView):
    def put(self, request, id, *args, **kwargs):
        try:
            task = Task.objects.get(id=id)
        except Task.DoesNotExist:
            return response_app(
                "Task not found", status_code=status.HTTP_404_NOT_FOUND, exception=True
            )
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            links = generate_hateoas_links(
                request, "tasks", task.id, request_type="put"
            )

            return response_app(
                status_code=status.HTTP_201_CREATED,
                data="Task updated successfully",
                obj=serializer.data,
                links=links,
            )
        return response_app(
            status_code=status.HTTP_400_BAD_REQUEST, exception=True, data="Invalid data"
        )
