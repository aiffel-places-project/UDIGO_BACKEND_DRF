import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from mixer.backend.django import mixer
from places.serializers import InferredPlaceImageSerializer
from places.tests.mocks import inference_mock
from places.models import KakaoPlace
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


@pytest.mark.parametrize("place", ["not", "allowed", "places"])
def test_place_curation_view_fail(client, place):
    create_test_infferd_images(50)
    client = get_admin_client_login(client)
    url = reverse("image-curation") + f"?place={place}"
    response = client.get(url)
    assert response.status_code == 200
    assert response.json() == []


def test_like_kakao_place(client, kakao_place_input):
    client = get_admin_client_login(client)
    url = reverse("likes-kakao")
    response = client.post(url, data=kakao_place_input)
    assert response.status_code == 201


def test_remove_like_kakao_place(client):
    user_1 = mixer.blend(get_user_model())
    kakao_place_liked = mixer.blend(KakaoPlace, like=[user_1])

    kakao_place_data = {
        "id": kakao_place_liked.id,
        "title": kakao_place_liked.title,
        "place_url": kakao_place_liked.place_url,
        "category_name": kakao_place_liked.category_name,
        "category_group_code": kakao_place_liked.category_group_code,
        "category_group_name": kakao_place_liked.category_group_name,
        "telephone": kakao_place_liked.telephone,
        "address": kakao_place_liked.address,
        "road_address": kakao_place_liked.road_address,
        "map_x": kakao_place_liked.map_x,
        "map_y": kakao_place_liked.map_y,
        "like": kakao_place_liked.like,
    }
    client.force_login(user_1)

    url = reverse("likes-kakao")
    response = client.post(url, data=kakao_place_data)
    assert response.status_code == 204


def test_like_tour_place(client, tour_place_input):
    client = get_admin_client_login(client)
    url = reverse("likes-tour")
    response = client.post(url, data=tour_place_input)
    assert response.status_code == 201
