from django.db import models

# Create your models here.
class Phone(models.Model):

    name = models.CharField(max_length=200)
    storage = models.IntegerField()
    storage_unit = models.CharField(max_length=50)
    color = models.CharField(max_length=100, blank=True)
    img = models.ImageField(upload_to=f'phones', blank=True)

    def __str__(self):
        return f'{self.name} {self.storage}{self.storage_unit}'