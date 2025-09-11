from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DaytripViewSet
from .views import ActivityViewSet
from .views import AttendeeViewSet

router = DefaultRouter()
router.register(r'daytrips', DaytripViewSet)
router.register(r'activity', ActivityViewSet)
router.register(r'attendees', AttendeeViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]