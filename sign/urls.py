from django.urls import path, include
from rest_framework.routers import DefaultRouter
from sign import views


router = DefaultRouter()
router.register(r'sign', views.SignViewSet, basename='sign')

urlpatterns = [
    path('', include(router.urls)),
]
