from rest_framework import serializers
from .models import (
    PlaceImage,
    KakaoPlace,
    TourPlace,
    UserLikeTourPlace,
    UserLikeKakaoPlace,
)
from users.serializers import UserSerializer


class PlaceImageSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = PlaceImage
        fields = "__all__"
