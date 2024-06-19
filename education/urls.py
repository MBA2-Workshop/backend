from django.urls import path, include
from rest_framework.routers import DefaultRouter
from education import views


router = DefaultRouter()
router.register(r'training', views.TrainingViewSet, basename='training')
router.register(r'student', views.CfaStudentViewSet, basename='student')
router.register(r'instructor', views.CfaInstructorViewSet, basename='instructor')

urlpatterns = [
    path('', include(router.urls)),
]
