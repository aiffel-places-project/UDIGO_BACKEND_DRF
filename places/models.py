from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField


class PlaceImage(models.Model):
    place_name = models.CharField(max_length=20)
    image = ResizedImageField(
        size=[600, 600], quality=95, upload_to="places/%Y/%m/%d", blank=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class TourPlace(models.Model):
    address = models.CharField(max_length=300, null=True)
    areacode = models.PositiveSmallIntegerField()
    cat1 = models.CharField(max_length=50)
    cat2 = models.CharField(max_length=50)
    cat3 = models.CharField(max_length=50)
    content_type_id = models.PositiveSmallIntegerField()
    createdtime = models.CharField(max_length=100)
    image1 = models.TextField(null=True)
    image2 = models.TextField(null=True)
    map_x = models.DecimalField(max_digits=9, decimal_places=6)
    map_y = models.DecimalField(max_digits=9, decimal_places=6)
    modifiedtime = models.CharField(max_length=100)
    sigungu_code = models.PositiveSmallIntegerField()
    telephone = models.CharField(max_length=100, null=True)
    title = models.CharField(max_length=200)
    overview = models.TextField(null=True)
    zipcode = models.IntegerField(null=True)
    homepage = models.TextField(null=True)

    user_like = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="user_like_tour_places_set", blank=True
    )

    class Meta:
        db_table = "tour_places"


class KakaoPlace(models.Model):
    title = models.CharField(max_length=200)  # place_name
    place_url = models.CharField(max_length=500)
    category_name = models.CharField(max_length=300)
    category_group_code = models.CharField(max_length=100)
    category_group_name = models.CharField(max_length=100)
    tel = models.CharField(max_length=100)  # phone
    address = models.CharField(max_length=300)  # address_name
    road_address = models.CharField(max_length=300)  # road_address_name
    mapx = models.DecimalField(max_digits=9, decimal_places=6)  # x
    mapy = models.DecimalField(max_digits=9, decimal_places=6)  # y

    user_like = models.ManyToManyField(
        User, through="UserLikeKakaoPlace", related_name="user_like_kakao_places_set"
    )

    class Meta:
        db_table = "kakao_places"


class Review(models.Model):
    place_type = models.CharField(max_length=50)  # enum field / kakao & tour
    place_tour = models.ForeignKey(TourPlace, null=True, on_delete=models.CASCADE)
    place_kakao = models.ForeignKey(KakaoPlace, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    grade = models.PositiveSmallIntegerField()
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "reviews"
