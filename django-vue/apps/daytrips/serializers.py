from rest_framework import serializers
from .models import Daytrip
from .models import Activity

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = "__all__"

class DaytripSerializer(serializers.ModelSerializer):
    activities = ActivitySerializer(many=True, read_only=True)
    class Meta:
        model = Daytrip
        fields = "__all__"