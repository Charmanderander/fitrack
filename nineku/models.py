from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime

class haikuDB(models.Model):
    first_verse = models.CharField(max_length=100)
    second_verse = models.CharField(max_length=100)
    third_verse = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(default=datetime.date.today())

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural=u'User profiles'
