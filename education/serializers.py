from user.models import User
from rest_framework import serializers
from education.models import Training, Grade
from event.models import Event


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


class CfaStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

    def create(self, validated_data):
        cfa = self.context['request'].user
        validated_data['cfa'] = cfa
        validated_data['role'] = 1

        return User.objects.create_user(**validated_data)


class CfaInstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

    def create(self, validated_data):
        cfa = self.context['request'].user
        validated_data['cfa'] = cfa
        validated_data['role'] = 2

        return User.objects.create_user(**validated_data)


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'

    def is_valid(self, *, raise_exception=False):
        user = self.context['request'].user
        self.initial_data['user'] = user.id
        student = User.objects.filter(
            id=self.initial_data.get('student')).first()
        event = Event.objects.filter(
            id=self.initial_data.get('event')).first()

        if event is None:
            raise serializers.ValidationError({
                "event": "The event is not provided."
            })
        training = event.training
        if training is None:
            raise serializers.ValidationError({
                "training": "The event does not have a training associated with it."
            })
        if student not in training.students.all():
            raise serializers.ValidationError({
                "student": "The student does not belong to this training class."
            })

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
        if attrs.get('coefficient') < 0:
            raise serializers.ValidationError({
                'event': 'Coefficient must be superior to 0'
            })
        return attrs
