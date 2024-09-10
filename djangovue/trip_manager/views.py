from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
#from .serializers import UserSerializer
import logging
# Create your views here.
def trip_detail(request, trip_id):
    # Process the trip_id
    # Fetch the corresponding trip from the database
    # Render the appropriate template
    return render(request, 'trips/detail.html', {'trip_id': trip_id})


@api_view(['POST'])
def something(request):
    return 0



