from django.urls import path, re_path
from . import views

urlpatterns = [
    path('trips/<int:trip_id>/', views.trip_detail, name='trip_detail'),
]