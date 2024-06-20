from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework import serializers
from user.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'cfa']


class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'role', 'cfa']

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role=3
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': super().to_representation(instance),
        }
        return data


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        attrs["username"] = attrs["email"]

        user = User.objects.filter(email=email).first()
        if user and user.check_password(password):
            if not user.is_active:
                raise serializers.ValidationError("User account is disabled.")
            attrs["username"] = user.username
            data = super().validate(attrs)
            refresh = self.get_token(user)

            data['user'] = {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role,
                'cfa': user.cfa.pk if user.cfa else None
            }
            data['refresh'] = str(refresh)
            data['access'] = str(refresh.access_token)
            return data
        else:
            raise serializers.ValidationError("Invalid email or password")


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    pass
