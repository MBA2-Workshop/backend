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
        return attrs
