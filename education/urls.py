from django.urls import path, include
from rest_framework.routers import DefaultRouter
from education import views


router = DefaultRouter()
router.register(r'training', views.TrainingViewSet, basename='training')
router.register(r'student', views.CfaStudentViewSet, basename='student')
router.register(r'instructor', views.CfaInstructorViewSet, basename='instructor')
router.register(r'sign', views.SignViewSet, basename='sign')
router.register(r'grade', views.GradeViewSet, basename='grade')

urlpatterns = [
    path('', include(router.urls)),
    path('trainings/', views.trainings_list, name='training-list'),
    path('instructors/', views.instructors_list, name='instructors-list'),
    path('grades/', views.grades_list, name='grades-list'),
]
