from rest_framework.viewsets import ModelViewSet
from reviews.serializers import KakaoPlaceReviewSerializer, TourPlaceReviewSerializer
from reviews.models import KakaoPlaceReview, TourPlaceReview


class KakaoPlaceReviewViewSet(ModelViewSet):
    serializer_class = KakaoPlaceReviewSerializer
    queryset = KakaoPlaceReview.objects.all()
    lookup_field = "id"


class TourPlaceReviewViewSet(ModelViewSet):
    serializer_class = TourPlaceReviewSerializer
    queryset = TourPlaceReview.objects.all()
    lookup_field = "id"
