from django.db import models
from django.db.models import Min
from django.db.models.functions import TruncDay
from django.contrib.auth.models import User
from decimal import Decimal

class Phone(models.Model):

    name = models.CharField(max_length=200)
    storage = models.IntegerField()
    storage_unit = models.CharField(max_length=50)
    color = models.CharField(max_length=100, blank=True)
    img = models.ImageField(upload_to=f'phones', blank=True)

    def __str__(self):
        return f'{self.name} {self.storage}{self.storage_unit} {self.color}'

    def get_all_offers(self):
        return self.offer_set.all()

    def get_all_lowest_offers(self):
        return self.offer_set.annotate(day=TruncDay('date')).values('day').annotate(Min('price')).order_by('-day')

    def get_lowest_price(self):
        return self.offer_set.aggregate(Min('price')).get('price__min')

    def get_current_lowest_price(self):
        sorted_offers = self.get_all_lowest_offers()
        if len(sorted_offers) > 0:
            newest_offer = sorted_offers[0]
            return newest_offer['price__min'] #TODO: for now hardcoded currency, fix it later

    def get_observed_starting_price(self, user_id):
        return ObservedPhone.get_observed_starting_price(phone_id=self.id, user_id=user_id)

    def follow(self, user_id):
        ObservedPhone.follow(phone_id=self.id, user_id=user_id)

    def unfollow(self, user_id):
        ObservedPhone.unfollow(phone_id=self.id, user_id=user_id)


class ObservedPhone(models.Model):
    phone = models.ForeignKey(Phone, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, default=None)

    @classmethod
    def follow(cls, phone_id, user_id):
        phone_to_observe = Phone.objects.get(id=phone_id)
        current_lowest_price = phone_to_observe.get_current_lowest_price()
        cls(phone_id=phone_id, user_id=user_id, price=current_lowest_price).save()

    @classmethod
    def unfollow(cls, phone_id, user_id):
        observed_phone = cls.objects.get(phone_id=phone_id, user_id=user_id)
        observed_phone.delete()

    @classmethod
    def get_user_observed_phones(cls, user_id):
        observed_phones_records = cls.objects.filter(user_id=user_id)
        phones = [record.phone for record in observed_phones_records]
        return phones

    @classmethod
    def get_observed_starting_price(cls, user_id, phone_id):
        return cls.objects.get(phone_id=phone_id, user_id=user_id).price


    class Meta:
        unique_together = (('phone', 'user'))

    def __str__(self):
        return f"<(Phone: {self.phone}), (User: {self.user})>"


class Shop(models.Model):
    
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='shops')
    url = models.URLField()

    def __str__(self):
        return self.name

class Offer(models.Model):
    
    date = models.DateTimeField() # phone price date
    price = models.DecimalField(max_digits=6, decimal_places=2)
    currency = models.CharField(max_length=3, default="zł") # currency in format https://en.wikipedia.org/wiki/ISO_4217
    phone = models.ForeignKey(Phone, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.get_date_str()} {self.phone} {self.price}'

    def get_date_str(self):
        return self.date.strftime('%Y-%m-%d')
