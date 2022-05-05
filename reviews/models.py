from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from common.models import CommonModel
from places.models import TourPlace, KakaoPlace


class Review(CommonModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("회원")
    )
    grade = models.PositiveSmallIntegerField(verbose_name=_("평점"))
    text = models.TextField(blank=True, verbose_name=_("리뷰"))

    class Meta:
        abstract = True


class KakaoPlaceReview(Review):
    place_kakao = models.ForeignKey(
        KakaoPlace, null=True, on_delete=models.CASCADE, verbose_name=_("카카오")
    )

    class Meta:
        db_table = "kakaoplace_review"


class TourPlaceReview(Review):
    place_tour = models.ForeignKey(
        TourPlace, null=True, on_delete=models.CASCADE, verbose_name=_("투어")
    )

    class Meta:
        db_table = "tourplace_review"
