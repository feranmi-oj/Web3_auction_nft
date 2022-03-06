from django.db import models
from djongo.models.fields import ObjectIdField
from datetime import datetime
from django.contrib.auth.models import User
from django.urls import reverse


class Profile(models.Model):
    _id = ObjectIdField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address_g = models.CharField(
        max_length=256,
        blank=False,
        null=False,
        unique=True,
        error_messages={"unique": "This address is already registered"},
    )
    token_amount = models.FloatField(default=0)
    dollar_amount = models.FloatField(default=0)
    ip_address = models.CharField(max_length=150, blank=True, null=True)
    last_login = models.DateTimeField(default=datetime.today())

    def __str__(self):
        return "{}".format(self.user.username)


class Artwork(models.Model):
    _id = ObjectIdField()
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    image = models.ImageField(blank=False, null=False)
    description = models.TextField()
    artwork_url = models.CharField(max_length=5000)
    artwork_hash = models.CharField(max_length=256, blank=True, null=False)
    starting_price = models.FloatField(default=0)
    token_offer = models.FloatField(default=0, blank=True, null=True)
    buy_now = models.FloatField(default=0)
    ending_auction = models.DateTimeField(auto_now_add=False, default=datetime.today())
    artist_address = models.CharField(max_length=256, blank=False, null=False)
    buyer = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=5, default="open")

    def get_id(self):
        return self._id

    def get_url(self):
        return reverse("app:make_an_offer", kwargs={"pk": self.pk})
