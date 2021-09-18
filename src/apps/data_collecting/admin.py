from django.contrib import admin

from . import models


@admin.register(models.OffersScrapingData)
class OffersScrapingDataAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "phone",
        "shop",
        "url"
    )