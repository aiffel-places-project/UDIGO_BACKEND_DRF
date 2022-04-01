import pytest
from mixer.backend.django import mixer
from utils.tests import User

pytestmark = pytest.mark.django_db


def test_create_user_by_mixer(User):
    user_1 = mixer.blend(User, email="test@test.com", social_type=1, nickname="test")
    assert user_1.nickname == "test"


def test_create_user_manually(User):
    User.objects.create(email="test@test.com", social_type=1, nickname="test")
    assert len(User.objects.all()) == 1


def test_create_superuser(User):
    superuser = User.objects.create_superuser(email="admin@admin.com")
    assert superuser.is_admin is True
