import requests
from django.contrib.auth import get_user_model


@pytest.fixture
def user_model():
    return get_user_model()


@pytest.fixture
def test_image():
    image_from_picsum = requests.get("https://picsum.photos/300/300")
    byte_image = image_from_picsum.content
    return byte_image
