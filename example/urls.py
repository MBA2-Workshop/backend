from django.urls import path, include
from rest_framework.routers import DefaultRouter
from example.models import Example
from example import views


router = DefaultRouter()
router.register(r'example', views.ExampleViewSet, basename='example')

urlpatterns = [
    path('', include(router.urls)),
]
