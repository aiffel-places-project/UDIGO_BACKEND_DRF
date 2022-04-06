import pytest
from unittest.mock import patch
from django.urls import reverse
from common.utils.tests import pytestmark
from users.tests.mocks import create_kakao_access_mock


def test_consent_to_kakao_access(client):
    url = reverse("kakao-access")
    response = client.get(url)
    assert response.status_code == 302


def test_kakao_callback(client, mocker):
    url = reverse("kakao-callback")
    mocker.patch('users.views.KakaoCallbackView._get_access_token_from_kakao', create_kakao_access_mock)
    response = client.get(url)
    assert response.status_code == 200