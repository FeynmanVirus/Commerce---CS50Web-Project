from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields.files import ImageField
from django.conf import settings
from datetime import date

CATEGORIES = [
    ("N", "No category"),
    ("F", "Fasion"),
    ("T", "Toys"),
    ("E", "Electronics"),
    ("H", "Home"),
    ("HW", "Hardware")
]
today = date.today()
today_string = f"{today.year}-{today.month}-{today.day}"
class User(AbstractUser):
    
    def __str__(self):
        return f"{self.username}"

class Listings(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,verbose_name="user", null=True, related_name="user")
    title = models.CharField(max_length=100, default='')
    description = models.CharField(max_length=1000, default='')
    price = models.IntegerField(null=False, default=0)
    image_link = models.URLField(max_length=1000, default='')
    category = models.CharField(max_length=200, default='', choices=CATEGORIES)
    active_state = models.BooleanField(default=False)
    winner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="winner", null=True, default=None, related_name="winner")
    date_created = models.DateField(default=today_string)

    def __str__(self):
        return f"""Username: {self.user} title: {self.title}, created: {self.date_created} description: {self.description}, price: {self.price}, 
        image: {self.image_link}, category: {self.category}, winner: {self.winner} active: {self.active_state}"""

class Bids(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="user", null=True, related_name="bids")
    listing = models.ForeignKey("Listings", on_delete=models.CASCADE, verbose_name="listing", null=True, related_name="listingbids")
    amount = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user} bid {self.amount} on {self.listing.title}"


class Comments(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="user", null=True, related_name="comments")
    comment = models.CharField(max_length=10000, default='')
    listing = models.ForeignKey("Listings", on_delete=models.CASCADE, verbose_name="listing", null=True, related_name="listingcomments")
    date = models.DateField(default=today_string)
    def __str__(self):
        return f"{self.user} commented: {self.comment} on {self.listing.title} on {self.date}"


class Watchlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="user", null=True, related_name="watchlist")
    listing = models.ForeignKey("Listings", on_delete=models.CASCADE, verbose_name="listing", null=True, related_name="listingwatchlist")
    watchlist_status = models.BooleanField(default=False)

    def __str__(self):
        if self.watchlist_status:
            return f"{self.user} has {self.listing} in their watchlist"
        else:
            return f"{self.user} does not have {self.listing} in their watchlist"