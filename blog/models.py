from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
import datetime

from django.utils import timezone

class Data(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=3000)
    location = models.CharField(max_length=100)
    time = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    distance = models.CharField(max_length=100)
    user = models.CharField(max_length=100,default="unknown user")
    datetime = models.DateTimeField(default=datetime.datetime.now())

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural=u'User profiles'

class Likes(models.Model):
    user = models.CharField(max_length=100,null=True,blank=True)
    postid = models.IntegerField(null=True,blank=True)
