import pytest
from decouple import config, Csv
from django.contrib.auth import get_user_model
from mixer.backend.django import mixer
from places.models import InferredPlaceImage


pytestmark = pytest.mark.django_db
name_list = (
    "공원",
    "공항",
    "놀이공원",
    "다리",
    "미술관",
    "볼링장",
    "산",
    "아이스링크",
    "아쿠아리움",
    "호텔",
    "궁궐",
    "지하철역",
    "놀이터",
    "수영장",
    "폭포",
    "동물원",
    "절",
    "교회",
    "성당",
    "시장",
    "쇼핑몰",
    "클럽",
    "박물관",
    "축구장",
    "야구장",
    "농구장",
    "공연장",
    "베이커리",
    "키즈카페",
    "숲",
    "캠핑장",
    "식물원",
    "해수욕장",
    "수상레포츠",
    "미용실",
    "PC방",
    "도서관",
    "컨벤션센터",
    "대학교",
    "패스트푸드점",
    "골프장",
    "헬스장",
    "병원",
    "빨래방",
    "찜질방",
    "스키장",
    "워터파크",
    "한옥마을",
    "롯데월드타워",
    "남산서울타워",
    "동대문디자인플라자",
    "63빌딩",
    "국회의사당",
    "청와대",
    "세빛섬",
)


def get_admin_client_login(client):
    user_model = get_user_model()
    user_1 = mixer.blend(user_model, is_admin=True)
    client.force_login(user_1)
    return client


def create_test_infferd_images(count):
    mixer.cycle(count).blend(
        InferredPlaceImage,
        predicted_place_name=(name for name in name_list),
    )
