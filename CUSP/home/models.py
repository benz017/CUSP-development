from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


# Create your models here.

class Events(models.Model):
    name = models.CharField(max_length=1000)
    start_date = models.DateTimeField(null=False,default=timezone.now)
    end_date = models.DateTimeField(null=True,default=timezone.now)
    location = models.CharField(max_length=300)
    event_pic = models.ImageField(upload_to='pics')
    event_thumbnail = models.ImageField(upload_to='thumbnail')
    instructors = models.CharField(max_length=200)
    solo_price = models.IntegerField(null=False, default=0)
    duet_price = models.IntegerField(null=True, default=0)
    tribe_price = models.IntegerField(null=True, default=0)
    earlybird_discount = models.IntegerField(null=False, default=0)
    earlybird_last_date = models.DateField(null=True,default=timezone.now)
    about = models.CharField(max_length=3000)
    about_instructor = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Subscribers(models.Model):
    email = models.EmailField(max_length=250,unique=True)

    def __str__(self):
        return self.email


class Email(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250, unique=True)
    contact_number = models.CharField(max_length=15)
    message = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatar', null=True, blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    username = models.CharField(max_length=30, blank=True)
    email = models.EmailField(max_length=150)
    contact_number = models.CharField(max_length=15, null=True)
    dob = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=150, blank=True, null=True)
    relationship_status = models.CharField(max_length=25, blank=True, null=True)
    languages = models.CharField(max_length=400, blank=True, null=True)
    places_visited = models.CharField(max_length=400, blank=True, null=True)
    emp_status = models.CharField(max_length=75, blank=True, null=True)
    profession = models.CharField(max_length=75, blank=True, null=True)
    passion = models.CharField(max_length=500, blank=True, null=True)
    diet = models.CharField(max_length=32, blank=True, null=True)
    allergic_food = models.CharField(max_length=300, blank=True, null=True)
    physical_activities = models.CharField(max_length=300, blank=True, null=True)
    health_problems = models.CharField(max_length=300, blank=True, null=True)
    personality = models.CharField(max_length=32, blank=True, null=True)
    signup_confirmation = models.BooleanField(default=False, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return "{}, {}, {}".format(self.username, self.email, self.signup_confirmation)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class ExpPayment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, null=True, related_name="payments")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=300, null=True)
    order_id = models.CharField(max_length=40, primary_key=True)
    order_type = models.CharField(max_length=30, null=True)
    amount = models.IntegerField(default=0)
    is_paid = models.BooleanField(default=False)
    payment_id = models.CharField(max_length=40)
    signature = models.CharField(max_length=256)

    def __str__(self):
        return "{}, {}, {}".format(self.order_id, self.payment_id, self.signature)
