import os
import requests
from google.oauth2 import id_token
from google.auth.transport import requests as google_request


class OauthKakao:
    # 유저 정보 가져오기
    def get_user_info(self, access_token):
        headers = {"Authorization": f"Bearer {access_token}"}
        url = "https://kapi.kakao.com/v2/user/me"
        response = requests.get(url, headers=headers)
        response = response.json()
        return response

    # 토큰 유효성 검사(토큰 정보 보기)
    def get_access_token_info(self, access_token):
        url = "https://kapi.kakao.com/v1/user/access_token_info"
        hearders = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=hearders)
        data = response.json()
        result = {
            # 'status_code': response.status_code,
            "code": data["code"]
            if "code" in data
            else 200
        }
        if response.status_code == 200:
            result["id"] = data["id"]
        elif data["code"] == -401:  # 유효하지 않은 앱키나 액세스 토큰으로 요청한 경우
            result["message"] = "EXPIRED_KAKAO_TOKEN"
        elif data["code"] == -1:  # 카카오 플랫폼 서비스의 일시적 내부 장애 상태
            result["message"] = "KAKAO_SERVER_ERROR"
        elif (
            data["code"] == -2
        ):  # 필수 인자가 포함되지 않은 경우나 호출 인자값의 데이터 타입이 적절하지 않거나 허용된 범위를 벗어난 경우
            result["message"] = "INVALID_VALUE"

        return result

    # 토큰 갱신
    def refresh_token(self, grant_type, client_id, refresh_token):
        url = "https://kapi.kakao.com/oauth/token"
        data = {
            "grant_type": grant_type,
            "client_id": client_id,
            "refresh_token": refresh_token,
        }
        response = requests.post(url, data=data)
        response = response.json()
        return response


class OauthGoogle:
    def get_token_info(self, token):
        try:
            idinfo = id_token.verify_oauth2_token(
                token, google_request.Request(), os.environ.get("GOOGLE_CLIENT_ID")
            )
            return {"code": 200, "id": idinfo["sub"], "name": idinfo["name"]}
        except ValueError as e:
            print(e)
            return {"code": 400, "message": "INVALID_TOKEN"}


class OauthApple:
    # 토큰 유효성 검사(토큰 정보 보기)
    def get_access_token_info(self, id_token):
        pass

    # 유저 정보 가져오기
    def get_user_info(self, access_token):
        pass
