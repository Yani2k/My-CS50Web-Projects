from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
  pass

class Listing_Category(models.Model):
  category_name = models.CharField(max_length=64)

class Listing(models.Model):
  seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sell_items")
  buyer = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name="bought_items")
  category = models.ForeignKey(Listing_Category, on_delete=models.CASCADE, related_name="category")
  minimal_bid = models.IntegerField()
  title = models.CharField(max_length=64, default="Default title")
  description = models.TextField(default="No description")
  closing_date = models.DateTimeField()
  photo = models.URLField(blank=True, null=True)
  
class Comment(models.Model):
  author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="comments_by")
  on = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments_on")
  when = models.DateTimeField()
   
class Bid(models.Model):
  bidder = models.ForeignKey(User, on_delete=models.CASCADE)
  amount = models.IntegerField()
  on = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
  when = models.DateTimeField()
  
