from django.urls import path
from .views import (
    ClassificationView,
    PlaceLikeView,
    UserLikeView,
    ImageSearchHistoryView,
    ImageCurationView,
)

urlpatterns = [
    path("upload/", ClassificationView.as_view()),
    path("likes/", PlaceLikeView.as_view()),
    path("user/likes/", UserLikeView.as_view()),
    path("history/", ImageSearchHistoryView.as_view()),
    path("curation/", ImageCurationView.as_view()),
]
