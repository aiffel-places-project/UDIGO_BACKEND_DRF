import json
import random
import cv2
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import PlaceImage
from users.models import User
from .serializers import PlaceImageSerializer

# ClassificationView 서버 분리전
class ClassificationView(APIView):
    # 이미지 리사이즈 함수
    def _resize_image(self, image_path, size):
        image = cv2.imdecode(
            np.fromstring(image_path.read(), np.uint8), cv2.IMREAD_UNCHANGED
        )
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (size, size))
        return image

    # 추론 함수
    def _inference(self, image_path):
        image = self._resize_image(image_path, 600)
        image2 = cv2.resize(image, (224, 224))
        image2 = image2[np.newaxis, :, :, :]
        pred = model.predict(image2, batch_size=1)
        return str(np.argmax(pred)), image

    def post(self, request):
        """
        기능 추가 - 내가 검색했던 내용 볼 수 있게끔? > 예측결과도 저장
        """
        img = request.FILES["image"]
        # 이미지 전처리 및 예측
        pred_index, save_image = self._inference(img)
        pred = label_info[pred_index]
        sen = random.choice(pred["sentence"])

        img.name = pred["category"] + "_" + str(np.random.randint(0, 9999999))

        if request.user.is_authenticated:
            # 유저가 올린 데이터를 저장
            user = User.objects.get(id=request.user.id)
            data = {"place_name": pred["category"], "image": img, "user": user}
            serializer = PlaceImageSerializer(data=data)
            if serializer.is_valid():
                save_image = serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"name": pred["category"], "sentence": sen}, status=status.HTTP_200_OK
        )


class PlaceLikeView:
    pass


class ImageSearchHistoryView:
    pass


class ImageCurationView:
    pass
