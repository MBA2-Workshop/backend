from rest_framework import serializers
from grade.models import Grade


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'

    def is_valid(self, *, raise_exception=False):
        user = self.context['request'].user
        self.initial_data['user'] = user.id

        if 'instructor' in self.initial_data:
            if user.role < 2:
                self.initial_data['instructor'] = None

        return super().is_valid(raise_exception=raise_exception)

    def validate(self, attrs):
        instructor = attrs.get('instructor')
        if instructor and instructor.role < 2:
            raise serializers.ValidationError({
                'instructor': 'Instructor must have a role of 2 or higher'
            })
        if attrs.get('value') < 0 or attrs.get('value') > 20:
            raise serializers.ValidationError({
                'value': 'Value must be between 0 and 20'
            })
        return attrs
