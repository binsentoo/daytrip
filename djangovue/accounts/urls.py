from django.urls import path
from . import views

urlpatterns = [
    path('getusers/', views.getData),
    path('adduser/',views.addUser)
]