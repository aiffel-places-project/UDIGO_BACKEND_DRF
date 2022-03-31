from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from common.models import CommonModel


class User(AbstractBaseUser, CommonModel):
    class SocialTypeChoice(models.IntegerChoices):
        KAKAO = 0
        APPLE = 1
        GOOGLE = 2

    social_type = models.IntegerField(choices=SocialTypeChoice.choices)
    nickname = models.CharField(max_length=25)

    class Meta:
        db_table = "users"
