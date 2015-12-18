from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime

class dreamDB(models.Model):
    dream = models.CharField(max_length=100)
    mood = models.CharField(max_length=100)
    tags = models.CharField(max_length=100)
    user = models.CharField(max_length=100,default="unknown user")

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(default=datetime.date.today())

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural=u'User profiles'
