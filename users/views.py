import requests
from django.conf import settings
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from users.services.social_login import get_access_token_from_kakao


def request_consent_to_kakao_access(request):
    url = settings.KAKAO_CONSENT_URL
    return redirect(url)


class KakaoCallbackView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):
        code = request.GET.get('code')
        results = self._get_access_token_from_kakao(code)
        response = Response(results, status=status.HTTP_200_OK)
        return response

    def _get_access_token_from_kakao(self, code):
        url = settings.KAKAO_ACCESS_URL + code
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(url, headers=headers).json()
        return response



class KakaoLogin(SocialLoginView):
    adapter_class = KakaoOAuth2Adapter
