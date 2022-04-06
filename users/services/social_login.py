import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)

# TODO: will be deleted
def get_access_token_from_kakao(code):
    url = settings.KAKAO_ACCESS_URL + code
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, headers=headers).json()
    return response


def get_kakao_user_profile(access_token):
    url = settings.KAKAO_PROFILE_URL
    try:
        profile = requests.get(
            url, headers={"Authorization": f"Bearer {access_token}"}
        ).json()
        return profile
    except ValueError as e:
        logger.info("Invalid Access Token")
        logger.error(e)
