from django.shortcuts import render
from rest_framework import viewsets
from .models import Daytrip
from .models import Activity
from .models import Attendee
from .serializers import DaytripSerializer
from .serializers import ActivitySerializer
from .serializers import AttendeeSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# Create your views here.
class DaytripViewSet(viewsets.ModelViewSet):
    queryset = Daytrip.objects.all()
    serializer_class = DaytripSerializer
    #permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'code'

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    #permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'id'

class AttendeeViewSet(viewsets.ModelViewSet):
    queryset = Attendee.objects.all()
    serializer_class = AttendeeSerializer