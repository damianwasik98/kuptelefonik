from django.db import models

# Create your models here.

from apps.dashboard.models import Phone, Shop

class OffersScrapingData(models.Model):
    phone = models.ForeignKey(Phone, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    url = models.URLField()

    def __str__(self):
        return f"{self.__class__.__name__} ({self.shop}, {self.phone})"

    class Meta:
        unique_together = ("phone", "shop")