from django.contrib import admin

from . import models

# Register your models here.
admin.site.register(models.Phone)
admin.site.register(models.ObservedPhone)
admin.site.register(models.Shop)
admin.site.register(models.Offer)
