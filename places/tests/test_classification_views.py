from pydoc import cli
import pytest
from django.urls import reverse
from mixer.backend.django import mixer
from places.serializers import InferredPlaceImageSerializer
from places.tests.mocks import inference_mock
from common.utils.tests import (
    get_admin_client_login,
    create_test_infferd_images,
    pytestmark,
    name_list,
)


def test_get_serializer(test_image):
    serializer = InferredPlaceImageSerializer(data={"image": test_image})
    assert serializer is not None


@pytest.mark.skip()
def test_place_classification_view(client, mocker, test_image):
    url = reverse("place-predict")
    mocker.patch("places.views.request_inference", inference_mock)
    client = get_admin_client_login(client)
    response = client.post(url, data={"image": test_image})
    assert response.status_code == 201


@pytest.mark.parametrize("place", name_list)
def test_place_curation_view(client, place):
    create_test_infferd_images(50)
    client = get_admin_client_login(client)
    url = reverse("image-curation") + f"?place={place}"
    response = client.get(url)
    assert response.status_code == 200
    assert response.json() != []


@pytest.mark.parametrize("place", ["not", "allowed", "places"])
def test_place_curation_view_fail(client, place):
    create_test_infferd_images(50)
    client = get_admin_client_login(client)
    url = reverse("image-curation") + f"?place={place}"
    response = client.get(url)
    assert response.status_code == 200
    assert response.json() == []
