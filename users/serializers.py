from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    social_type = serializers.CharField(max_length=30)

    class Meta:
        model = User
        fields = ("id", "nickname", "social_type")
        read_only_fields = ("id",)

    def create(self, validated_data):
        social_types = ["kakao", "google", "apple"]
        social_type = validated_data.get("social_type")
        social_type_id = social_types.index(social_type)

        validated_data["social_type"] = social_type_id
        user = super().create(validated_data)
        user.save()
        return user
