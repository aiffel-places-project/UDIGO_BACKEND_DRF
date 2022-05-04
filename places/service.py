import requests
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response


def request_inference(self, image):
    response = requests.post(settings.ML_SERVER_URL, files={"image": image})
    data = response.json()
    return data


def like_or_remove_like(request, queryset=None):
    id = request.data.get("id")
    user = request.user
    queryset = queryset.filter(id=id)
    if queryset:
        place = queryset.first()
        if user not in place.like.all():
            place.like.add(user)
            place.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            place.like.remove(user)
            place.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
