from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class User(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.username

    @classmethod
    def create_user(cls, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = cls.objects.normalize_email(email)
        user = cls(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=cls._db)
        return user

    @classmethod
    def create_superuser(cls, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return cls.create_user(username, email, password, **extra_fields)
