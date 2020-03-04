from django.db import models
from datetime import datetime

# Create your models here.


class Events(models.Model):
    name = models.CharField(max_length=1000)
    start_date = models.DateTimeField(null=False,default=datetime.now)
    end_date = models.DateTimeField(null=True,default=datetime.now)
    location = models.CharField(max_length=300)
    event_pic = models.ImageField(upload_to='pics')
    event_thumbnail = models.ImageField(upload_to='thumbnail')
    instructors = models.CharField(max_length=200)
    solo_price = models.IntegerField(null=False, default=0)
    duet_price = models.IntegerField(null=True, default=0)
    tribe_price = models.IntegerField(null=True, default=0)
    earlybird_discount = models.IntegerField(null=False, default=0)
    earlybird_last_date = models.DateField(null=True,default=datetime.now)
    about = models.CharField(max_length=3000)
    about_instructor = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Subscribers(models.Model):
    email = models.EmailField(max_length=250)

    def __str__(self):
        return self.email
