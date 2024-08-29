from django.db import models

class Person(models.Model):
    isDriver = models.BooleanField()

class Driver(Person):
    pass