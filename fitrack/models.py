from django.db import models

class Suggestion(models.Model):
    class Meta:
        app_label = "fitrack"
    name = models.CharField(max_length=30)
    suggestion = models.CharField(max_length=200)
