from django.contrib import admin

# Register your models here.

from .models import Secrets

admin.site.register(Secrets)
