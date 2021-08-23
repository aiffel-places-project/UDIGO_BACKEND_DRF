from .models import User
from .oauth import OauthKakao, OauthGoogle, OauthApple
from django.http import JsonResponse

SOCIAL_TYPE = ['kakao', 'apple', 'google']


def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            token = request.headers.get("Authorization")
            if token is not None:
                type, token = token.split(" ")
            else:
                type = token = None

            if type == "kakao":
                response = OauthKakao().get_access_token_info(token)
            elif type == "google":
                response = OauthGoogle().get_token_info(token)
            elif type == "apple":
                response = OauthApple().get_access_token_info(token)
            else:
                if "/place/upload" in request.get_raw_uri():
                    response = {"code": 200, "id": None}
                else:
                    return JsonResponse(
                        {"message": "INVALID_VALUE"}, status=400
                    )  # INVALID_TYPE

            if response['code'] == 200:
                if response['id'] is not None:
                    user = User.objects.get(social_type=SOCIAL_TYPE.index(type), social_id=response['id'])
                    request.user = user
                return func(self, request, *args, **kwargs)
            else:
                return JsonResponse({"message": response["message"]}, status=400)

        except User.DoesNotExist:
            return JsonResponse({"message": "INVALID_USER"}, status=400)
        except ValueError:
            return JsonResponse({"message": "INVALID_TOKEN"}, status=400)

    return wrapper
