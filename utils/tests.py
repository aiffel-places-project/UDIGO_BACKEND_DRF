import pytest
from django.contrib.auth import get_user_model


@pytest.fixture
def User():
    return get_user_model()
