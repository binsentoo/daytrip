from django.db import models
import string
import random

def generate_unique_code():
    length = 6
    chars = string.ascii_uppercase + string.digits  # A-Z and 0-9

    while True:
        code = ''.join(random.choices(chars, k=length))
        if not Daytrip.objects.filter(code=code).exists():
            return code

class Daytrip(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='itineraries')
    title = models.CharField(max_length=32)
    desc = models.TextField(blank=True)
    date = models.DateField()
    #host = models.CharField(max_length=32)
    code = models.CharField(max_length=10, unique=True, primary_key=True,default=generate_unique_code)

class Activity(models.Model):
    daytrip = models.ForeignKey(
        Daytrip,
        on_delete=models.CASCADE,
        related_name='activities',
        to_field='code'
    )
    name = models.CharField(max_length=128)
    location = models.TextField(blank=True)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    #end_time = models.TimeField(null=True, blank=True)
    #duration = models.DurationField(null=True, blank=True)
    note = models.TextField(blank = True)

class Attendee(models.Model):
    daytrip = models.ForeignKey(
        Daytrip,
        on_delete=models.CASCADE,
        related_name="attendees",
    )
    name = models.CharField(max_length=32)
    is_going = models.BooleanField(default=False)
    is_driver = models.BooleanField(default=False)