from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from places.models import InferredPlaceImage


# TODO: serializer 수정
class InferredPlaceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = InferredPlaceImage
        fields = ("predicted_place_name", "image", "user")
        read_only_fields = ("predicted_place_name", "user")

    def validate_image(self, image):
        size = image.size
        MAX_SIZE = 5000000
        if size > MAX_SIZE:
            exception = DjangoValidationError(_("사진의 크기는 5MB를 넘길 수 없습니다."))
            raise serializers.ValidationError(
                detail=serializers.as_serializer_error(exception)
            )
        return image
