from django.contrib import admin
from places.models import InferredPlaceImage


@admin.register(InferredPlaceImage)
class InferredPlaceImageAdmin(admin.ModelAdmin):
    pass
