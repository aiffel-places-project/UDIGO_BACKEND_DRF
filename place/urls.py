from django.urls import path
from .views import (
    Classification,
    PlaceReviewView,
    UserReviewView,
    PlaceLikeView,
    UserLikeView,
    ImageSearchHistoryView,
    ImageCurationView,
)

urlpatterns = [
    path("/upload", Classification.as_view()),
    path("/review/<int:review_id>", UserReviewView.as_view()),
    path("/review", UserReviewView.as_view()),
    path("/<int:place_id>/review", PlaceReviewView.as_view()),
    path("/like", PlaceLikeView.as_view()),
    path("/user/like", UserLikeView.as_view()),
    path("/history", ImageSearchHistoryView.as_view()),
    path("/curation", ImageCurationView.as_view()),
]
