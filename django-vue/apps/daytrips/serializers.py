from rest_framework import serializers
from .models import Daytrip
from .models import Activity
from .models import Attendee

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = "__all__"

    def validate(self, data):
        """
        Ensure open time ends before close time.
        """

        opens = data.get("opens_at", getattr(self.instance, "opens_at", None))
        closes = data.get("closes_at", getattr(self.instance, "closes_at", None))

        if opens is not None and closes is not None and closes <= opens:
            raise serializers.ValidationError(
                {"closes_at": "Closing time must be after opening time."}
            )
        
        return data


class AttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendee
        fields = "__all__"

class DaytripSerializer(serializers.ModelSerializer):
    activities = ActivitySerializer(many=True, read_only=True)
    attendees = AttendeeSerializer(many=True, read_only=True)
    class Meta:
        model = Daytrip
        fields = "__all__"