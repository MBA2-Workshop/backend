import datetime
from django.utils import timezone
from rest_framework import serializers
from event.models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

    def is_valid(self, *, raise_exception=False):
        user = self.context['request'].user
        self.initial_data['user'] = user.id

        if 'instructor' in self.initial_data:
            if user.role < 2:
                self.initial_data['instructor'] = None

        if user.role < 2:
            self.initial_data['training'] = None
            self.initial_data['type'] = 1

        start_date = datetime.datetime.strptime(
        self.initial_data.get('start_date'), '%Y-%m-%dT%H:%M:%S')
        end_date = datetime.datetime.strptime(
        self.initial_data.get('end_date'), '%Y-%m-%dT%H:%M:%S')

        if start_date > end_date:
            raise serializers.ValidationError({
                'start_date': 'Start date must be before end date'
            })

        return super().is_valid(raise_exception=raise_exception)

    def validate(self, attrs):
        instructor = attrs.get('instructor')
        if instructor and instructor.role < 2:
            raise serializers.ValidationError({
                'instructor': 'Instructor must have a role of 2 or higher'
            })
        if attrs.get('training') and attrs.get('type') != 2:
            raise serializers.ValidationError({
                'type': 'Type must be 2 for training events'
            })
        if attrs.get('type') == 2 and not attrs.get('training'):
            raise serializers.ValidationError({
                'training': 'Training is required for training events'
            })
        return attrs

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['start_date'] = instance.start_date.strftime('%Y-%m-%dT%H:%M:%S')
        data['end_date'] = instance.end_date.strftime('%Y-%m-%dT%H:%M:%S')
        return data
