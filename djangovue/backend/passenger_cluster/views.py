from django.shortcuts import render
from .models import Person

def index(request):
    return render(request, 'index.html')

def home(request):
    #all_people = Person.objects.all
    return render(request, 'home.html', {})

