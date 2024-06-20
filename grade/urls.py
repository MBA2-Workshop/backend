from django.urls import path, include
from rest_framework.routers import DefaultRouter
from grade import views


router = DefaultRouter()
router.register(r'grade', views.GradeViewSet, basename='grade')

urlpatterns = [
    path('', include(router.urls)),
]
