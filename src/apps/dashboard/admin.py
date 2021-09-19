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
        "scraping_data_count",
    )

    list_editable = (
        "name",
        "storage",
        "storage_unit",
        "color",
    )

    search_fields = ("name",)

    list_filter = (
        "storage",
        "color",
    )

    inlines = [
        OffersScrapingDataInline
    ]

    autocomplete_fields = ("color",)

    def scraping_data_count(self, phone_obj):
        scraping_data_count = len(
            phone_obj.offersscrapingdata_set.filter(phone_id=phone_obj.id)
        )
        return scraping_data_count


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

    search_fields = ("name",)


@admin.register(models.Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "date",
        "shop",
        "phone",
        "price",
        "currency",
        "url"
    )

    list_filter = (
        "shop",
        "phone",
    )


@admin.register(models.StorageUnit)
class StorageUnitAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Color)
class ColorAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(models.Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "code",
        "display_name",
        "country",
    )

    list_editable = (
        "display_name",
        "country",
    )