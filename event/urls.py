from django.urls import path, include
from rest_framework.routers import DefaultRouter
from event.models import Event
from event import views


router = DefaultRouter()
router.register(r'event', views.EventViewSet, basename='event')

urlpatterns = [
    path('', include(router.urls)),
]
