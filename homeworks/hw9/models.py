from django.db import models
from django.utils import timezone

# Create your models here.

class BlogHW9(models.Model):
    name = models.CharField(max_length=20)
    text = models.CharField(max_length=200)
    timestamp = models.DateTimeField('timestamp', default=timezone.now)

    class Meta:
        permissions = (
            ("see_post", "Can see post"),
            ("create_post", "Can create post"),
            ("modifiy_post", "Can change post"),
            ("delete_post", "Can remove a post"),
        )

    def __str__(self):
        return str(self.name) + " wrote comment: " + str(self.text) + " on " + str(self.timestamp)
