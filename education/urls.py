from django.urls import path, include
from rest_framework.routers import DefaultRouter
from education import views


router = DefaultRouter()
router.register(r'training', views.TrainingViewSet, basename='training')

urlpatterns = [
    path('', include(router.urls)),
]
