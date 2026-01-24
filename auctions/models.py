from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField("Lot", blank=True, related_name="subscribers")

class Category(models.Model):
    name = models.CharField(max_length=32)
    default_image = models.URLField()

    def __str__(self):
        return self.name

class Lot(models.Model):
    name = models.CharField(max_length=128)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lots")
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="lots")
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_bid = models.ForeignKey("Bid", on_delete=models.SET_NULL, null=True, blank=True, related_name="current_for_lot")
    is_active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    image_url = models.URLField(null=True, blank=True, default=None)

    def __str__(self):
        return f"Lot: {self.id}, {self.name} listed by {self.owner}. Active: {self.is_active}"

class Bid(models.Model):
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bid#{self.id} listed by {self.bidder} at {self.timestamp}. ${self.amount}"

class Comment(models.Model):
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE, related_name="comments") 
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.owner} on Lot#{self.lot.id} says: {self.content[:20]}"