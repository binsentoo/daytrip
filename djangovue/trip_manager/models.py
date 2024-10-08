from django.db import models
from django.utils import timezone
# Create your models here.

class Trip(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    #events = models.ManyToManyField(Event)
    UID = models.CharField(max_length=6, primary_key=True)
    @property 
    def final_min_cost(self):
        return sum(event.min_cost for event in self.events.all())
    @property
    def final_max_cost(self):
        return sum(event.max_cost for event in self.events.all())
        #WIP
    @property
    def start_time(self):
        first_event = self.events.order_by('start_time').first()
        return first_event.start_time if first_event else None
    @property
    def end_time(self):
        last_event = self.events.order_by('-end_time').first()
        return last_event.end_time if last_event else None
    def expire_trip(self):
        if self.end_time < timezone.now():
            self.active = False
            self.save()

class Event(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField(auto_now_add=False)
    end_time = models.DateTimeField(auto_now_add=False)
    location= models.CharField(max_length=256)
    min_cost = models.DecimalField(max_digits=10, decimal_places=2)
    max_cost = models.DecimalField(max_digits=10, decimal_places=2)
    #temperature = models.FloatField(null=True, blank=True) IGNORE
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='events')
