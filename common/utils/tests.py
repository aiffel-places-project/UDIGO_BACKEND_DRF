import pytest
from django.contrib.auth import get_user_model
from mixer.backend.django import mixer

pytestmark = pytest.mark.django_db


def get_admin_client_login(client):
    user_model = get_user_model()
    user_1 = mixer.blend(user_model, is_admin=True)
    client.force_login(user_1)
    return client
