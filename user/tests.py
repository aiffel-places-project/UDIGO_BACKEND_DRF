from django.views import View
from django.http import JsonResponse
from django.test import Client, TestCase
from unittest.mock import Mock, MagicMock
from django.forms.models import model_to_dict

from .models import User
from .utils import OauthKakao, OauthGoogle


class UserTest(TestCase):
    def setUp(self):
        User.object.create(
            social_type=0,
            social_id='999999999999',
            nickname='user'
        )

    def tearDown(self):
        User.objects.all().delete()

    def test_kakao_login_success(self):
        pass

    def test_kakao_login_fail(self):
        pass
