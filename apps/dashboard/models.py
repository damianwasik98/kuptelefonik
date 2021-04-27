from django.db import models

# Create your models here.
class Phone(models.Model):

    name = models.CharField(max_length=200)
    storage = models.IntegerField()
    storage_unit = models.CharField(max_length=50)
    color = models.CharField(max_length=100, blank=True)
    img = models.ImageField(upload_to=f'phones', blank=True)
    observed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} {self.storage}{self.storage_unit}'

    def follow(self):
        self.observed = True
        self.save()

    def unfollow(self):
        self.observed = False
        self.save()

class Shop(models.Model):
    
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='shops')
    url = models.URLField()

    def __str__(self):
        return self.name

class Offer(models.Model):
    
    date = models.DateTimeField() # phone price date
    price = models.DecimalField(max_digits=6, decimal_places=2)
    currency = models.CharField(max_length=3) # currency in format https://en.wikipedia.org/wiki/ISO_4217
    phone = models.ForeignKey(Phone, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.phone} {self.price}'