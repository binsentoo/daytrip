from django.shortcuts import render
from django.http import HttpResponse
def homepage(request):
    return render(request, 'home.html')


def about(request):
    return HttpResponse("Hello World, about!")


def index(request):
    return render(request, 'index.html')