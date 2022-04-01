import pytest
from mixer.backend.django import mixer
from common.utils.tests import user_model

pytestmark = pytest.mark.django_db


def test_create_user_model_by_mixer(user_model):
    user_model_1 = mixer.blend(
        user_model, email="test@test.com", social_type=1, nickname="test"
    )
    assert user_model_1.nickname == "test"


def test_create_user_model_manually(user_model):
    user_model.objects.create(email="test@test.com", social_type=1, nickname="test")
    assert len(user_model.objects.all()) == 1


def test_create_superuser_model(user_model):
    superuser_model = user_model.objects.create_superuser_model(email="admin@admin.com")
    assert superuser_model.is_admin is True
