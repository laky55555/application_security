from django.db import models

# Create your models here.

class Secrets(models.Model):
    name = models.CharField(max_length=20)
    text = models.CharField(max_length=200)
    secret_key = models.CharField(max_length=20, default="secret")

    def __str__(self):
        return str(self.name) + " has secret: " + str(self.text)
