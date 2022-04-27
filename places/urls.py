from django.urls import path
from places.views import PlaceImageClassificationView


urlpatterns = [
    path("inference/", PlaceImageClassificationView.as_view(), name="place-predict")
]
