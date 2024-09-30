from rest_framework import serializers
from trip_manager.models import Event, Trip

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'name', 'description', 'start_time', 'end_time', 'location', 'min_cost', 'max_cost']

class TripSerializer(serializers.ModelSerializer):
    events = EventSerializer(many=True)

    class Meta:
        model = Trip
        fields = ['name', 'description', 'events', 'UID']

    def create(self, validated_data):
        events_data = validated_data.pop('events')
        trip = Trip.objects.create(**validated_data)
        for event_data in events_data:
            event = Event.objects.create(trip=trip, **event_data)
        return trip

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['final_min_cost'] = instance.final_min_cost
        representation['final_max_cost'] = instance.final_max_cost
        representation['start_time'] = instance.start_time
        representation['end_time'] = instance.end_time
        return representation
    '''
    class Meta:
        model = Trip
        fields = '__all__' '''