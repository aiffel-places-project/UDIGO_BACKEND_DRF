from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField
from common.models import CommonModel


class InferredPlaceImage(CommonModel):
    predicted_place_name = models.CharField(max_length=20, verbose_name=_("예측 장소 이름"))
    image = ResizedImageField(
        size=[600, 600],
        quality=95,
        upload_to="places/%Y/%m/%d",
        blank=True,
        verbose_name=_("저장 이미지"),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("회원")
    )

    class Meta:
        db_table = "inferred place"


class TourPlace(CommonModel):
    address = models.CharField(max_length=300, null=True, verbose_name=_("주소"))
    areacode = models.PositiveSmallIntegerField(verbose_name=_("지역번호"))
    cat1 = models.CharField(max_length=50, verbose_name=_("카테고리1"))
    cat2 = models.CharField(max_length=50, verbose_name=_("카테고리2"))
    cat3 = models.CharField(max_length=50, verbose_name=_("카테고리3"))
    content_type_id = models.PositiveSmallIntegerField(verbose_name=_("컨텐츠 유형 번호"))
    image1 = models.TextField(null=True, verbose_name=_("이미지1"))
    image2 = models.TextField(null=True, verbose_name=_("이미지2"))
    map_x = models.DecimalField(max_digits=9, decimal_places=6, verbose_name=_("x좌표"))
    map_y = models.DecimalField(max_digits=9, decimal_places=6, verbose_name=_("y좌표"))
    created_time = models.CharField(max_length=100, verbose_name=_("생성 시간"))
    modifiedtime = models.CharField(max_length=100, verbose_name=_("수정 시간"))
    sigungu_code = models.PositiveSmallIntegerField(verbose_name=_("시군구 코드"))
    telephone = models.CharField(max_length=100, null=True, verbose_name=_("전화번호"))
    title = models.CharField(max_length=200, verbose_name=_("장소 이름"))
    overview = models.TextField(null=True, verbose_name=_("오버뷰"))
    zipcode = models.IntegerField(null=True, verbose_name=_("우편번호"))
    homepage = models.TextField(null=True, verbose_name=_("홈페이지"))
    like = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="user_like_tour_places_set",
        blank=True,
        verbose_name=_("좋아요"),
    )

    class Meta:
        db_table = "tour_places"


class KakaoPlace(CommonModel):
    title = models.CharField(max_length=200, verbose_name=_("장소 이름"))
    place_url = models.CharField(max_length=500, verbose_name=_("URL"))
    category_name = models.CharField(max_length=300, verbose_name=_("카테고리 이름"))
    category_group_code = models.CharField(max_length=100, verbose_name=_("카테고리 그룹 번호"))
    category_group_name = models.CharField(max_length=100, verbose_name=_("카테고리 그룹 이름"))
    telephone = models.CharField(max_length=100, verbose_name=_("전화번호"))
    address = models.CharField(max_length=300, verbose_name=_("주소"))
    road_address = models.CharField(max_length=300, verbose_name=_("도로명 주소"))
    map_x = models.DecimalField(max_digits=9, decimal_places=6, verbose_name=_("x좌표"))
    map_y = models.DecimalField(max_digits=9, decimal_places=6, verbose_name=_("y좌표"))
    like = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="user_like_kakao_places_set",
        blank=True,
        verbose_name=_("좋아요"),
    )

    class Meta:
        db_table = "kakao_places"
