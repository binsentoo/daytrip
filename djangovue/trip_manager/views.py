from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import TripSerializer, EventSerializer
from .models import Trip, Event
import logging
logger = logging.getLogger(__name__)

# Create your views here.
def trip_detail(request, trip_id):
    # Process the trip_id
    # Fetch the corresponding trip from the database
    # Render the appropriate template
    return render(request, 'trips/detail.html', {'trip_id': trip_id})


@api_view(['GET'])
def getTrip(request, UID):
    try:
        trip = Trip.objects.get(UID=UID)
        serializer = TripSerializer(trip)
        return Response(serializer.data, status=200)
    except Trip.DoesNotExist:
        return Response({"error": "Trip not found"}, status=404)
def getEvent(request, UID):
    try:
        event = Event.objects.get(UID=UID)
        serializer = EventSerializer(event)
        return Response(serializer.data, status=200)
    except Event.DoesNotExist:
        return Response({"error": "Event not found"}, status=404)

@api_view(['POST'])
def addTrip(request):
    logger.info(f"Received data: {request.data}")
    serializer = TripSerializer(data=request.data)
    if serializer.is_valid():
        try:
            trip = serializer.save()
            logger.info("Trip created")
            return Response(serializer.data, status=201)
        except Exception as e:
            logger.error(f"Error saving user: {str(e)}")
            return Response({"error": str(e)}, status=500)
    else:
        logger.error(f"Serializer errors: {serializer.errors}")
        return Response(serializer.errors, status=400)




