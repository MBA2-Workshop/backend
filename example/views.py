from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from example.models import Example
from example.serializers import ExampleSerializer


class ExampleViewSet(viewsets.ViewSet):
    # Exemple d'un viewset sur la route /example qui permet de lister, créer, modifier, supprimer des examples
    # Serializer à utiliser, ici ExampleSerializer
    serializer_class = ExampleSerializer
    # Modèle à utiliser, ici Example
    model = Example
    # Liste des méthodes HTTP autorisées
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    # Liste des permissions à appliquer, ici l'utilisateur doit être connecté
    permission_classes = [IsAuthenticated]

    def list(self, request):
        # Récupérer tous les examples
        queryset = self.model.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        # Créer un nouvel example
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        # Récupérer un example par son id, /example/<id>/
        instance = self.model.objects.get(pk=pk)
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

    def update(self, request, pk=None):
        # Modifier un example par son id, /example/<id>/, méthode PUT
        instance = self.model.objects.get(pk=pk)
        serializer = self.serializer_class(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        # Modifier partiellement un example par son id, /example/<id>/, méthode PATCH
        instance = self.model.objects.get(pk=pk)
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    # Le delete provient de l'héritage de viewsets.ViewSet, /example/<id>
