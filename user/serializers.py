from rest_framework.serializers import ModelSerializer
from .models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "created_at", "updated_at", "is_active"]
        read_only_fields = ["id", "password"]
