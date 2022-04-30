from django.db.models import Q
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response
from places.serializers import InferredPlaceImageSerializer
from places.models import InferredPlaceImage
from places.service import request_inference


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


class PlaceImageSearchHistoryView:
    pass


class PlaceLikeView:
    pass
