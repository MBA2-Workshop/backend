from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from user.permissions import IsInstructor
from education.models import Training
from education.serializers import TrainingSerializer


class TrainingViewSet(viewsets.ViewSet):
    serializer_class = TrainingSerializer
    model = Training
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    permission_classes = [IsInstructor]

    def create(self, request):
        context = {'request': request}
        serializer = self.serializer_class(data=request.data, context=context)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        queryset = self.model.objects.filter(cfa=request.user).all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        training = self.model.objects.filter(cfa=request.user, pk=pk).first()
        if not training:
            return Response({"message":"Training not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(training)
        return Response(serializer.data)

    def update(self, request, pk=None):
        context = {'request': request}
        instance = self.model.objects.filter(pk=pk, cfa=request.user).first()
        if not instance:
            return Response(
                data={"message": "Training not found"},
                status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(instance, data=request.data, context=context)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        context = {'request': request}
        instance = self.model.objects.filter(pk=pk, cfa=request.user).first()
        if not instance:
            return Response(
                data={"message": "Training not found"},
                status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(instance, data=request.data, partial=True, context=context)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        instance = self.model.objects.filter(pk=pk, cfa=request.user).first()
        if not instance:
            return Response(
                data={"message": "Training not found"},
                status=status.HTTP_404_NOT_FOUND)
        self.perform_destroy(instance)
        return Response(data={"message": "Training deleted"}, status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()