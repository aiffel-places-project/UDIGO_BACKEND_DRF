from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.views import View
from django.http import JsonResponse

from .models import User
from .serializers import UserSerializer
from .utils import OauthKakao, OauthGoogle
from django.forms.models import model_to_dict


SOCIAL_TYPE = ["kakao", "naver", "google"]


class FakeKakaoResponse:
    response = {
        "id": 12345,
        "properties": {"nickname": "test_user"},
    }


class LoginView(APIView):
    def post(self, request):
        try:
            token = request.headers.get("Authorization")
            social_type, token = token.split(" ")
            social_type = social_type.lower()

            if not token:
                return Response(
                    {"MESSAGE": "INVALID_TOKEN"}, status=status.HTTP_400_BAD_REQUEST
                )

            if social_type == "kakao":
                user_data = {"social_type": SOCIAL_TYPE.index(social_type)}
                kakao = OauthKakao()
                valid_result = kakao.get_access_token_info(access_token=token)
                if valid_result["code"] == 200:
                    user_info = kakao.get_user_info(access_token=token)
                    user_data["social_id"] = str(user_info["id"])
                    user_data["nickname"] = user_info["properties"]["nickname"]
                else:
                    return Response(
                        {"MESSAGE": valid_result["message"]},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            elif social_type == "google":
                user_data = {"social_type": SOCIAL_TYPE.index(social_type)}
                google = OauthGoogle()
                valid_result = google.get_token_info(token=token)
                if valid_result["code"] == 200:
                    user_data["social_id"] = valid_result["id"]
                    user_data["nickname"] = valid_result["name"]
                else:
                    return Response(
                        {"MESSAGE": valid_result["message"]},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            elif social_type == "apple":
                pass

            elif social_type.split("_")[0] == "test":
                if social_type.split("_")[1] == "kakao":
                    user_data = {"social_type": 0}
                    user_data["social_id"] = str(FakeKakaoResponse.response["id"])
                    user_data["nickname"] = FakeKakaoResponse.response["properties"][
                        "nickname"
                    ]
            else:
                return Response(
                    {"MESSAGE": "INVALID_SOCIAL_TYPE"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # sign in
            user = User.objects.filter(
                social_type=user_data["social_type"], social_id=user_data["social_id"]
            )
            if user.exists():
                user = user.values()[0]
                serializer = UserSerializer(data=user)
                if serializer.is_valid():
                    login = serializer.data
                    login["social_type"] = SOCIAL_TYPE[login["social_type"]]
                    return Response(login, status=status.HTTP_200_OK)
            # sign up
            else:
                serializer = UserSerializer(data=user_data)
                if serializer.is_valid():
                    create_user = serializer.save()
                    create_user = UserSerializer(create_user).data
                    create_user["social_type"] = SOCIAL_TYPE[create_user["social_type"]]
                    return Response(create_user, status=status.HTTP_201_CREATED)
                else:
                    return Response(
                        serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )
        except ValueError:
            return Response(
                {"MESSAGE": "INVALID_TOKEN"}, status=status.HTTP_400_BAD_REQUEST
            )
