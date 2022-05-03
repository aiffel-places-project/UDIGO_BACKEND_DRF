from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers


def raise_serializer_error(message):
    exception = DjangoValidationError(_(message))
    raise serializers.ValidationError(detail=serializers.as_serializer_error(exception))
