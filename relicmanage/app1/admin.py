from django.contrib import admin

# Register your models here.

from app1 import models
from . import models

admin.site.register(models.User)