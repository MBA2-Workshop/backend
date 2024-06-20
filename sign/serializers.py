from rest_framework import serializers
from django.utils import timezone
from .models import Sign
from user.models import User
from education.models import Training
from event.models import Event

class SignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sign
        fields = ['id', 'label', 'user', 'training', 'event', 'date', 'signed']

    def is_valid(self, *, raise_exception=False):
        user = self.context['request'].user
        self.initial_data['user'] = user.id

        event_id = self.initial_data.get('event')
        if event_id:
            event = Event.objects.get(id=event_id)
            actual_time = timezone.now()
            if event.end_date < actual_time or actual_time < event.start_date:
                raise serializers.ValidationError({
                    'event': 'Event is not active.'
                })

        return super().is_valid(raise_exception=raise_exception)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['date'] = instance.date.strftime('%Y-%m-%dT%H:%M:%S')
        return data
