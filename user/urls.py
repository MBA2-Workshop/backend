from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user.views import UserViewSet, CustomTokenObtainPairView, \
    CustomTokenRefreshView, SignupView
from user import views


router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('password/', views.set_new_password_token, name='set_new_password_token'),
]
