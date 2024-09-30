from django.urls import path
from . import views

urlpatterns = [
    path('trips/<int:trip_id>/', views.trip_detail, name='trip_detail'),
    path('gettrip/<str:UID>/', views.getTrip),
    #path('getevent/<str:UID>/', views.getEvent),
    path('addtrip/', views.addTrip),
]
