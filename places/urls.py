from django.urls import path
from places.views import (
    PlaceImageClassificationView,
    PlaceImageCurationView,
    KaKaoPlaceLikeView,
)


urlpatterns = [
    path("inference/", PlaceImageClassificationView.as_view(), name="place-predict"),
    path("curation/", PlaceImageCurationView.as_view(), name="image-curation"),
    path("likes/kakao/", KaKaoPlaceLikeView.as_view(), name="likes-kakao"),
]
