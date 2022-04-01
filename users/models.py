from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from common.models import CommonModel
from users.managers import UserManager


class User(AbstractBaseUser, CommonModel):
    class SocialTypeChoice(models.IntegerChoices):
        KAKAO = 0
        APPLE = 1
        GOOGLE = 2

    email = models.EmailField(max_length=255, unique=True, verbose_name=_("이메일"))
    social_type = models.IntegerField(
        choices=SocialTypeChoice.choices, verbose_name=_("소셜로그인"), blank=True, null=True
    )
    nickname = models.CharField(
        max_length=25, blank=True, null=True, verbose_name=_("닉네임")
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["social_type", "nickname"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        db_table = "users"
