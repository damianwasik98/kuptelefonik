from django.contrib import admin

from . import models


@admin.register(models.Phone)
class PhoneAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "storage",
        "storage_unit",
        "color",
        "img"
    )

    list_editable = (
        "name",
        "storage",
        "storage_unit",
        "color"
    )


@admin.register(models.ObservedPhone)
class ObservedPhoneAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "phone",
        "user",
        "date",
        "price"
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
        "url"
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
