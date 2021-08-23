from rest_framework import serializers
from .model import (
    PlaceImage,
    TourPlace,
    KakaoPlace,
    Review,
    UserLikeKakaoPlace,
    UserLikeTourPlace,
)
from user.serializers import UserSerializer


class PlaceImageSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = PlaceImage
        fields = "__all__"
        read_only_fields = ("user",)
