from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "nickname", "social_id", "social_type")
        read_only_fields = ("id",)

    def create(self, validated_data):
        user = super().create(validated_data)
        user.save()
        return user
