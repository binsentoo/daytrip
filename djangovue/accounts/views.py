from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User
from .serializers import UserSerializer
import logging
# Create your views here.
logger = logging.getLogger(__name__)

@api_view(['GET'])
def getData(request):
    people = User.objects.all()
    ser = UserSerializer(people, many=True)
    return Response(ser.data)


@api_view(['POST'])
def addUser(request):
    logger.info(f"Received data: {request.data}")
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        try:
            user = serializer.save()
            logger.info(f"User created: {user}")
            return Response(serializer.data, status=201)
        except Exception as e:
            logger.error(f"Error saving user: {str(e)}")
            return Response({"error": str(e)}, status=400)
    else:
        logger.error(f"Serializer errors: {serializer.errors}")
        return Response(serializer.errors, status=400)