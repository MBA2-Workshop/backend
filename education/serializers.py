import datetime
from django.utils import timezone
from rest_framework import serializers
from education.models import Training


class TrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Training
        fields = '__all__'

    def is_valid(self, *, raise_exception=False):
        user = self.context['request'].user
        self.initial_data['cfa'] = user.id

        return super().is_valid(raise_exception=raise_exception)

    def validate(self, attrs):
        if attrs['students']:
            for student in attrs['students']:
                if student.role != 1:
                    raise serializers.ValidationError({
                        "students":"Only students can be added to a training"
                    })
        return attrs
