from django.db import models
from django.utils import timezone
from pgcrypto_expressions.fields import EncryptedTextField

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

class BlogColumnEncryptHW9(models.Model):
    name = models.CharField(max_length=20)
    text = EncryptedTextField()
    timestamp = models.DateTimeField('timestamp', default=timezone.now)

    class Meta:
        permissions = (
            ("see_post_encrypted", "Can see post encrypted"),
            ("create_post_encrypted", "Can create post encrypted"),
            ("modifiy_post_encrypted", "Can change post encrypted"),
            ("delete_post_encrypted", "Can remove a post encrypted"),
        )

    def __str__(self):
        return str(self.name) + " wrote comment: " + str(self.text) + " on " + str(self.timestamp)
