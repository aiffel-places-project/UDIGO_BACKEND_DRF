from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from places.models import InferredPlaceImage, KakaoPlace
from common.utils.errors import raise_serializer_error


class InferredPlaceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = InferredPlaceImage
        fields = ("predicted_place_name", "image", "user", "created_at")
        read_only_fields = ("predicted_place_name", "user", "created_at")

    def validate_image(self, image):
        size = image.size
        MAX_SIZE = 5000000
        if size > MAX_SIZE:
            raise_serializer_error("사진의 크기는 5MB를 넘길 수 없습니다.")
        return image


class KakaoPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = KakaoPlace
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")

    def validate(self, attrs):
        for key in attrs.keys():
            if key not in KakaoPlace.__dict__.keys():
                raise_serializer_error("올바른 데이터를 넣어주세요.")

        attrs["like"].append(self.context["request"].user)
        return attrs
