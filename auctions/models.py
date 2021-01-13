from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime


class User(AbstractUser):
    pass


class category(models.Model) : 
    name = models.CharField(max_length=64)
    def __str__(self):
         return f"{self.name}"
 
class auction(models.Model):
    title= models.CharField(max_length = 64)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=3)
    image_url = models.CharField(max_length= 200)
    category = models.ForeignKey(category, on_delete = models.CASCADE, blank = True, related_name= "category")
    description = models.TextField(default='')
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete = models.CASCADE, related_name="creater")
    is_active = models.BooleanField(default='')
   
    def __str__(self):
         return f"{self.title} {self.starting_bid} {self.image_url} {self.category} {self.description} {self.created_by} {self.created_on}{self.is_active}  "


class activelisting(models.Model):   
    active = models.ManyToManyField(auction, blank = True,  related_name= "watchlist")
    watcher = models.ForeignKey(User,default= '', on_delete= models.CASCADE , related_name= "listwatcher")
    def __str__(self):
          return f"{self.active} "



class bid(models.Model):
    bid_value = models.IntegerField(default='')
    on_auction = models.ForeignKey(auction,on_delete= models.CASCADE, related_name= "bid_on_auction")
    created_by = models.ForeignKey(User, on_delete = models.CASCADE,  related_name= "bid_suggestion")
    def __str__(self):
         return f"{self.bid_value} {self.on_auction}{self.created_by}" 

class comment(models.Model):
    comment_text = models.TextField(default='')
    on_auction = models.ForeignKey(auction, on_delete = models.CASCADE, related_name= "comment_on_auction")
    created_by = models.ForeignKey(User, on_delete = models.CASCADE, related_name="commet_owner")
    def __str__(self):
         return f"{self.comment_text} {self.on_auction}{self.created_by}" 
