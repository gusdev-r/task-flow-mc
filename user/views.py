from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer
from .models import User
from _manager.utils import generate_hateoas_links, response_app
from rest_framework import generics
from rest_framework.views import status


class UsersListView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        links = generate_hateoas_links(
            request=request, resource_name="user", obj_id=None, request_type="get"
        )

        return response_app(
            data="List of users retrieved successfully",
            obj=serializer.data,
            links=links,
        )


class UsersListActiveView(APIView):
    def get(self, request):
        users = User.objects.filter(is_active=True)
        serializer = UserSerializer(users, many=True)
        links = generate_hateoas_links(
            request=request, resource_name="user", request_type="get"
        )
        return response_app(
            data="List of active users retrieved successfully",
            obj=serializer.data,
            links=links,
        )


class UsersCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            user_id = serializer.data.get("id")
            links = generate_hateoas_links(
                request=request,
                obj_id=user_id,
                resource_name="user",
                request_type="post",
            )

            return response_app(
                status_code=status.HTTP_201_CREATED,
                data="User created successfully!",
                obj=serializer.data,
                links=links,
            )

        except Exception as exc:
            return response_app(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                exception=True,
                data=str(exc),
            )


class UserDetailView(APIView):
    def get(self, request, user_id, *args, **kwargs):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return response_app(
                status_code=status.HTTP_404_NOT_FOUND,
                exception=True,
                data="User not found",
            )

        serializer = UserSerializer(user)
        links = generate_hateoas_links(
            request=request, resource_name="user", obj_id=user_id, request_type="get"
        )

        return response_app(
            data="User details retrieved successfully",
            obj=serializer.data,
            links=links,
        )


class UsersUpdateView(APIView):
    def put(self, request, user_id, *args, **kwargs):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return response_app(
                "User not found", status_code=status.HTTP_404_NOT_FOUND, exception=True
            )
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            links = generate_hateoas_links(
                request=request,
                resource_name="user",
                obj_id=user_id,
                request_type="put",
            )

            return response_app(
                status_code=status.HTTP_201_CREATED,
                data="User updated successfully",
                obj=serializer.data,
                links=links,
            )
        return response_app(
            status_code=status.HTTP_400_BAD_REQUEST, exception=True, data="Invalid data"
        )


class UserDeleteView(APIView):
    def delete(self, request, user_id, *args, **kwargs):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return response_app(
                "User not found", status_code=status.HTTP_404_NOT_FOUND, exception=True
            )
        user.delete()
        links = generate_hateoas_links(
            request=request, resource_name="user", obj_id=user_id, request_type="delete"
        )

        return response_app(
            status_code=status.HTTP_204_NO_CONTENT,
            data="User deleted successfully",
            links=links,
        )
