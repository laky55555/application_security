from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Money(models.Model):
    account = models.IntegerField(default=0)
    person = models.ForeignKey(User, unique=True)

    def __str__(self):
        return str(self.person) + " has $" + str(self.account)
