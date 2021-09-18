from django.contrib import admin

from . import models
from apps.data_collecting.models import OffersScrapingData

class OffersScrapingDataInline(admin.TabularInline):
    model = OffersScrapingData

@admin.register(models.Phone)
class PhoneAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "storage",
        "storage_unit",
        "color",
        "img",
    )

    list_editable = (
        "name",
        "storage",
        "storage_unit",
        "color",
    )

    search_fields = [
        "name",
    ]

    list_filter = (
        "storage",
        "color",
    )

    inlines = [
        OffersScrapingDataInline
    ]

@admin.register(models.ObservedPhone)
class ObservedPhoneAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "phone",
        "user",
        "date",
        "price",
    )

    list_filter = (
        "phone",
        "user",
    )


@admin.register(models.Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "url",
        "logo",
    )

    list_editable = (
        "name",
        "url",
    )


@admin.register(models.Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "date",
        "shop",
        "phone",
        "price",
        "currency",
    )

    list_filter = (
        "shop",
        "phone",
    )
