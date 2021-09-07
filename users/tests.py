from rest_framework.test import (
    APIClient,
    APITestCase,
)
from rest_framework import status
from .serializers import UserSerializer
from .models import User

# from unittest.mock import patch, MagicMock


class SocialSignUpTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_kakao_sign_up(self):
        self.client.credentials(HTTP_AUTHORIZATION="test_kakao " + "FakeToken")
        sign_up_url = "/users/login/"
        response = self.client.post(sign_up_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["social_type"], "kakao")

    def test_kakao_login(self):
        test_kakao_user_data = {
            "social_type": 0,
            "social_id": "12345",
            "nickname": "test_user",
        }
        serializer = UserSerializer(data=test_kakao_user_data)
        if serializer.is_valid():
            self.test_kakao_user = serializer.save()

        self.client.credentials(HTTP_AUTHORIZATION="test_kakao " + "FakeToken")

        login_url = "/users/login/"
        response = self.client.post(login_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["social_type"], "kakao")
