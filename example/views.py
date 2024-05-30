from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from example.models import Example
from example.serializers import ExampleSerializer


class ExampleViewSet(viewsets.ViewSet):
    serializer_class = ExampleSerializer
    model = Example
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = self.model.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        instance = self.model.objects.get(pk=pk)
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

    def update(self, request, pk=None):
        instance = self.model.objects.get(pk=pk)
        serializer = self.serializer_class(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        instance = self.model.objects.get(pk=pk)
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)