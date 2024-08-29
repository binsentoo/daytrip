from django.db import models

class Person(models.Model):
    fname = models.CharField(max_length=250)
    lname = models.CharField(max_length=250)
    #email = models.EmailField(max_length=250)
    #password = 
    home_address = models.CharField(max_length=250)
    isDriver = models.BooleanField()
    def __str__(self):
        return self.fname + ' ' + self.lname

class Driver(Person):
    pass