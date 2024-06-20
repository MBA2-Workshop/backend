from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
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
        if request.user.role == 2:
            # if user is an instructor
            queryset = self.model.objects.filter(
                Q(user=request.user) | Q(instructor=request.user) | Q(training__instructor=request.user)
            ).distinct()
        if request.user.role == 1:
            # if user is a student
            queryset = self.model.objects.filter(
                Q(user=request.user) | Q(training__students=request.user)
            ).distinct()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        instance = self.model.objects.filter(pk=pk, user=request.user).first()
        if request.user.role == 2:
            queryset = self.model.objects.filter(
                Q(pk=pk) & (Q(user=request.user) | Q(instructor=request.user) | Q(training__instructor=request.user))
            ).distinct()
            instance = queryset.first()
        if request.user.role == 1:
            queryset = self.model.objects.filter(
                Q(pk=pk) & (Q(user=request.user) | Q(training__students=request.user))
            ).distinct()
            instance = queryset.first()
        if not instance:
            return Response(
                data={"message": "Event not found"},
                status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

    def update(self, request, pk=None):
        context = {'request': request}
        instance = self.model.objects.filter(pk=pk, user=request.user).first()
        if not instance:
            return Response(
                data={"message": "Event not found"},
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
                data={"message": "Event not found"},
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
                data={"message": "Event not found"},
                status=status.HTTP_404_NOT_FOUND)
        self.perform_destroy(instance)
        return Response(data={"message": "Event deleted"}, status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def unique_events_list(request):
    training_id = request.query_params.get('training')
    events = Event.objects.filter(training_id=training_id).distinct('label').all()
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)
