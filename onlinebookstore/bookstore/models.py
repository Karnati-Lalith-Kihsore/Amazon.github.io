from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime


# Create your models here.
class User(AbstractUser):
    pass

class Listing(models.Model):
    seller = models.ForeignKey("User", on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=5000)
    price = models.IntegerField()
    timestamp = models.DateTimeField(default=datetime.now())
    image = models.URLField(null=True)

    def __str__(self):
        return f"{self.id} {self.name}"
    
class Cart(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    listing = models.ForeignKey("Listing", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=datetime.now())

class Buy(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    listing = models.ForeignKey("Listing", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=datetime.now())

class User_details(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    houseno = models.CharField(max_length=64)
    streetno = models.CharField(max_length=64)
    village = models.CharField(max_length=64)
    district = models.CharField(max_length=64)
    state = models.CharField(max_length=64)
    pincode = models.IntegerField()
    phonenumber = models.IntegerField()