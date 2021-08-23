from rest_framework import serializers
from .model import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("created_at", "social_id")
