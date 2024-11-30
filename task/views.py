from django.shortcuts import render
from rest_framework import generics
from .serializers import TaskSerializer
from .models import Task, TaskConfig
from django.http import JsonResponse
from rest_framework.views import status, Response
from rest_framework.exceptions import NotFound
from _manager.utils import response_app


class TaskListAllView(generics.ListAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()


class TaskRetrieveView(generics.RetrieveAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    lookup_field = "id"


class TaskCreateView(generics.CreateAPIView):
    serializer_class = TaskSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        response_app(serializer.data, status_code=404, exception=True)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class TaskRetriveUpdateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    lookup_field = "id"

    def destroy(self, request, *args, **kwargs):
        try:
            object = self.get_object()
            object.delete()

            return response_app(
                "The task was deleted", status_code=200, exception=False
            )

        except NotFound:
            return response_app("Task not found", status_code=404, exception=True)
