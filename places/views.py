from django.db.models import Q
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView, ListCreateAPIView
from rest_framework.response import Response
from common.permissions import IsMe
from places.serializers import (
    InferredPlaceImageSerializer,
    KakaoPlaceSerializer,
    TourPlaceSerializer,
)
from places.models import InferredPlaceImage, KakaoPlace, TourPlace
from places.service import request_inference, like_or_remove_like


class PlaceImageClassificationView(GenericAPIView):
    serializer_class = InferredPlaceImageSerializer
    queryset = InferredPlaceImage.objects.all()

    def post(self, request):
        image = self.request.FILES.get("image")
        serializer = self.get_serializer(data={"image": image})
        serializer.is_valid(raise_exception=True)

        inferred_data = request_inference(image)
        merged_data = {
            "image": image,
            "predicted_place_name": inferred_data["label_category"],
            "sentence": inferred_data["sentence"],
        }

        self.perform_create(serializer, merged_data)
        response = self.get_response(inferred_data)
        return response

    def perform_create(self, serializer, data):
        serializer.save(
            user=self.request.user,
            image=data["image"],
            predicted_place_name=data["predicted_place_name"],
        )

    def get_response(self, data):
        response = Response(
            {
                "predicted_place_name": data["label_category"],
                "sentence": data["sentence"],
            },
            status=status.HTTP_201_CREATED,
        )
        return response


class PlaceImageCurationView(ListAPIView):
    serializer_class = InferredPlaceImageSerializer
    queryset = InferredPlaceImage.objects.all()

    def get_queryset(self):
        place = self.request.GET.get("place")

        other_place = InferredPlaceImage.objects.filter(
            ~Q(user=self.request.user) & Q(predicted_place_name=place)
        )
        if other_place_count := other_place.count() < 20:
            other_place = other_place[:other_place_count]
        return other_place


class PlaceImageHistoryView(ListAPIView):
    serializer_class = InferredPlaceImageSerializer
    permission_classes = [IsMe]

    def get_queryset(self):
        queryset = InferredPlaceImage.objects.objects.filter(
            user=self.request.user
        ).order_by("-created_at")
        return queryset


class KaKaoPlaceLikeView(ListCreateAPIView):
    """
    카카오 API에서 가져온 장소 정보
    POST: 좋아요를 누르면 DB에 장소를 저장 및 좋아요 추가
    GET: 좋아요를 누른 장소 READ
    """

    serializer_class = KakaoPlaceSerializer
    queryset = KakaoPlace.objects.all()
    permission_classes = [IsMe]

    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if response := like_or_remove_like(request, queryset):
            return response
        return super().post(request)

    def get_queryset(self):
        if self.request.method == "GET":
            user = self.request.user
            queryset = KakaoPlace.objects.filter(like__in=[user])
            return queryset
        return super().get_queryset()


class TourPlaceLikeView(ListCreateAPIView):
    """
    Tour API에서 가져온 장소 정보
    POST: 좋아요를 누르면 DB에 장소를 저장 및 좋아요 추가
    GET: 좋아요를 누른 장소 READ
    """

    serializer_class = TourPlaceSerializer
    queryset = TourPlace.objects.all()
    permission_classes = [IsMe]

    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if response := like_or_remove_like(request, queryset):
            return response
        return super().post(request)

    def get_queryset(self):
        if self.request.method == "GET":
            user = self.request.user
            queryset = TourPlace.objects.filter(like__in=[user])
            return queryset
        return super().get_queryset()
