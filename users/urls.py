from django.urls import path
from users.views import request_consent_to_kakao_access, KakaoCallbackView


urlpatterns = [
    path("social-login/kakao/", request_consent_to_kakao_access, name="kakao-access"),
    path("social-login/kakao/callback/", KakaoCallbackView.as_view(), name="kakao-callback")
]
