from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from event.models import Event
from event.serializers import EventSerializer


class EventViewSet(viewsets.ViewSet):
    serializer_class = EventSerializer
    model = Event
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    permission_classes = [IsAuthenticated]

    def create(self, request):
        context = {'request': request}
        serializer = self.serializer_class(data=request.data, context=context)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        queryset = self.model.objects.filter(user=request.user).all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        instance = self.model.objects.filter(pk=pk, user=request.user).first()
        if not instance:
            return Response(
                data={"message": "not found"},
                status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

    def update(self, request, pk=None):
        context = {'request': request}
        instance = self.model.objects.filter(pk=pk, user=request.user).first()
        if not instance:
            return Response(
                data={"message": "not found"},
                status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(instance, data=request.data, context=context)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        context = {'request': request}
        instance = self.model.objects.filter(pk=pk, user=request.user).first()
        if not instance:
            return Response(
                data={"message": "not found"},
                status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(instance, data=request.data, partial=True, context=context)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        instance = self.model.objects.filter(pk=pk, user=request.user).first()
        if not instance:
            return Response(
                data={"message": "not found"},
                status=status.HTTP_404_NOT_FOUND)
        self.perform_destroy(instance)
        return Response(data={"message": "deleted"}, status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
