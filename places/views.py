import requests
from django.conf import settings
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from places.serializers import InferredPlaceImageSerializer
from places.models import InferredPlaceImage


class PlaceImageClassificationView(GenericAPIView):
    serializer_class = InferredPlaceImageSerializer
    queryset = InferredPlaceImage.objects.all()

    def request_inference(self, image):
        response = requests.post(settings.ML_SERVER_URL, files={"image": image})
        data = response.json()
        return data

    def post(self, request):
        image = self.request.FILES.get("image")
        serializer = self.get_serializer(data={"image": image})
        serializer.is_valid(raise_exception=True)

        inferred_data = self.request_inference(image)
        data = {
            "image": image,
            "predicted_place_name": inferred_data["label_category"],
            "sentence": inferred_data["sentence"],
        }
        serializer.save(
            user=request.user,
            image=data["image"],
            predicted_place_name=data["predicted_place_name"],
        )
        return Response(
            {
                "predicted_place_name": inferred_data["label_category"],
                "sentence": inferred_data["sentence"],
            },
            status=status.HTTP_201_CREATED,
        )


class PlcaeImageSearchHistoryView:
    pass


class PlcaeImageCurationView:
    pass


class PlaceLikeView:
    pass
