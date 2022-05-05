from rest_framework.routers import DefaultRouter
from reviews.views import KakaoPlaceReviewViewSet, TourPlaceReviewViewSet


router = DefaultRouter()
router.register("places/kakao/", KakaoPlaceReviewViewSet)
router.register("places/tour/", TourPlaceReviewViewSet)


urlpatterns = []
urlpatterns += router.urls
