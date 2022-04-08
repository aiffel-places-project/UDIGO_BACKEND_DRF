import requests
from django.conf import settings
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from common.utils.logger import logger


def request_consent_to_kakao_access(request):
    url = settings.KAKAO_CONSENT_URL
    return redirect(url)


class KakaoCallbackView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):
        code = request.GET.get("code")
        results = self._get_access_token_from_kakao(code)
        response = Response(results, status=status.HTTP_200_OK)
        return response

    def _get_access_token_from_kakao(self, code):
        url = settings.KAKAO_ACCESS_URL + code
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(url, headers=headers).json()
        return response


class KakaoLoginView(SocialLoginView):
    adapter_class = KakaoOAuth2Adapter
    social_type = 0

    def get_response(self):
        self._insert_user_data_to_instance()
        return super().get_response()

    def _insert_user_data_to_instance(self):
        self.user.nickname = self._get_nickname()
        self.user.social_type = self.social_type
        self.user.save()

    def _get_nickname(self):
        access_token = self.request.data["access_token"]
        profile = self._get_kakao_user_profile(access_token)
        nickname = profile["kakao_account"]["profile"]["nickname"]
        return nickname

    def _get_kakao_user_profile(self, access_token):
        url = settings.KAKAO_PROFILE_URL
        try:
            profile = requests.get(
                url, headers={"Authorization": f"Bearer {access_token}"}
            ).json()
            return profile
        except ValueError as e:
            logger.info("Invalid Access Token")
            logger.error(e)
