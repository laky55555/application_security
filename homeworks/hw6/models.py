from django.db import models
from django.utils import timezone

# Create your models here.

class Blog(models.Model):
    name = models.CharField(max_length=20)
    text = models.CharField(max_length=200)
    timestamp = models.DateTimeField('timestamp', default=timezone.now)

    def __str__(self):
        return str(self.name) + " wrote comment: " + str(self.text) + " on " + str(self.timestamp)
