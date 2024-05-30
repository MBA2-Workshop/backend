from django.urls import path, include
from rest_framework.routers import DefaultRouter
from example.models import Example
from example import views


router = DefaultRouter()
# Exemple d'un viewset sur la route /example qui permet de lister, créer, modifier, supprimer des examples
router.register(r'example', views.ExampleViewSet, basename='example')

urlpatterns = [
    # Inclure les routes du router
    path('', include(router.urls)),
]
