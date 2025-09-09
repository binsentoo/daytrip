from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DaytripViewSet
from .views import ActivityViewSet

router = DefaultRouter()
router.register(r'daytrips', DaytripViewSet)
router.register(r'activity', ActivityViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]