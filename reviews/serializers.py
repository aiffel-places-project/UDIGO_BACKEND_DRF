from rest_framework import serializers
from reviews.models import KakaoPlaceReview, TourPlaceReview


class KakaoPlaceReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = KakaoPlaceReview
        fields = "__all__"
        read_only_fields = ("user", "place_kakao")


class TourPlaceReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourPlaceReview
        fields = "__all__"
        read_only_fields = ("user", "place_tour")
