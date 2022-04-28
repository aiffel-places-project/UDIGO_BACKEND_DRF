import requests
from django.conf import settings


def request_inference(self, image):
    response = requests.post(settings.ML_SERVER_URL, files={"image": image})
    data = response.json()
    return data
