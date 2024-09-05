from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User
from .serializers import UserSerializer
# Create your views here.


@api_view(['GET'])
def getData(request):
    people = User.objects.all()
    ser = UserSerializer(people, many=True)
    return Response(ser.data)


@api_view(['POST'])
def addUser(request):
    serializer = UserSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)