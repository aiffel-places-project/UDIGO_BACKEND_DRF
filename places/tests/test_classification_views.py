import pytest
from django.urls import reverse
from places.serializers import InferredPlaceImageSerializer
from places.tests.mocks import inference_mock
from common.utils.tests import get_admin_client_login, pytestmark


def test_get_serializer(test_image):
    serializer = InferredPlaceImageSerializer(data={"image": test_image})
    assert serializer is not None


@pytest.mark.skip()
def test_place_classification_view(client, mocker, test_image):
    url = reverse("place-predict")
    mocker.patch('places.views.request_inference', inference_mock)
    client = get_admin_client_login(client)
    response = client.post(url, data={"image": test_image})
    assert response.status_code == 201
