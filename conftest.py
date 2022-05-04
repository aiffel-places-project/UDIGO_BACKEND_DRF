import requests
import pytest
from django.contrib.auth import get_user_model


@pytest.fixture
def user_model():
    return get_user_model()


@pytest.fixture
def test_image():
    image_from_picsum = requests.get("https://picsum.photos/300/300")
    byte_image = image_from_picsum.content
    return byte_image


@pytest.fixture
def kakao_place_input():
    kakao_place_data = {
        "id": 3333,
        "title": "test",
        "place_url": "http://test.com",
        "category_name": "test",
        "category_group_code": "test",
        "category_group_name": "test",
        "telephone": "010-1234-4567",
        "address": "test",
        "road_address": "test",
        "map_x": 132.123,
        "map_y": 64.124,
        "like": [],
    }
    return kakao_place_data


@pytest.fixture
def tour_place_input():
    tour_place_data = {
        "id": 0,
        "address": "string",
        "areacode": 0,
        "cat1": "string",
        "cat2": "string",
        "cat3": "string",
        "content_type_id": 0,
        "image1": "string",
        "image2": "string",
        "map_x": 132.123,
        "map_y": 64.124,
        "created_time": "string",
        "modifiedtime": "string",
        "sigungu_code": 0,
        "telephone": "string",
        "title": "string",
        "overview": "string",
        "zipcode": 0,
        "homepage": "string",
        "like": [],
    }
    return tour_place_data
