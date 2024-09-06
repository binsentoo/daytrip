from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(models.Model):
    address = models.CharField(max_length=256)
    fname = models.CharField(max_length=256)
    lname = models.CharField(max_length=256)