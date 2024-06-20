from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from user.models import User
from user.permissions import IsInstructor, IsCfa
from education.models import Training
from education.serializers import TrainingSerializer, CfaStudentSerializer, \
    CfaInstructorSerializer
from user.utils import set_token_send_email


class TrainingViewSet(viewsets.ViewSet):
    """
    ViewSet for CFA (or Instructor) to manage training
    """

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


class CfaStudentViewSet(viewsets.ViewSet):
    """
    ViewSet for CFA to manage students
    """

    serializer_class = CfaStudentSerializer
    model = User
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    permission_classes = [IsCfa]

    def list(self, request):
        queryset = self.model.objects.filter(cfa=request.user, role=1).all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        student = self.model.objects.filter(cfa=request.user, role=1, pk=pk).first()
        if not student:
            return Response({"message":"Student not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(student)
        return Response(serializer.data)

    def create(self, request):
        context = {'request': request}
        serializer = self.serializer_class(data=request.data, context=context)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            set_token_send_email(serializer.instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        context = {'request': request}
        instance = self.model.objects.filter(pk=pk, cfa=request.user, role=1).first()
        if not instance:
            return Response(
                data={"message": "Student not found"},
                status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(instance, data=request.data, context=context)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        context = {'request': request}
        instance = self.model.objects.filter(pk=pk, cfa=request.user, role=1).first()
        if not instance:
            return Response(
                data={"message": "Student not found"},
                status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(instance, data=request.data, partial=True, context=context)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        instance = self.model.objects.filter(pk=pk, cfa=request.user, role=1).first()
        if not instance:
            return Response(
                data={"message": "Student not found"},
                status=status.HTTP_404_NOT_FOUND)
        self.perform_destroy(instance)
        return Response(data={"message": "Student deleted"}, status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trainings_list(request):
    """
    List all trainings
    """
    if request.user.role == 1:
        # if user is student
        trainings = Training.objects.filter(students=request.user).all()
    elif request.user.role == 2:
        # if user is instructor
        trainings = Training.objects.filter(instructor=request.user).all()
    else:
        # if user is cfa
        trainings = Training.objects.filter(cfa=request.user).all()

    serializer = TrainingSerializer(trainings, many=True)
    return Response(serializer.data)


class CfaInstructorViewSet(viewsets.ViewSet):
    """
    ViewSet for CFA to manage instructors
    """

    serializer_class = CfaInstructorSerializer
    model = User
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    permission_classes = [IsInstructor]

    def list(self, request):
        queryset = self.model.objects.filter(cfa=request.user, role=2).all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        instructor = self.model.objects.filter(cfa=request.user, role=2, pk=pk).first()
        if not instructor:
            return Response({"message":"Instructor not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(instructor)
        return Response(serializer.data)

    def create(self, request):
        context = {'request': request}
        serializer = self.serializer_class(data=request.data, context=context)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            set_token_send_email(serializer.instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        context = {'request': request}
        instance = self.model.objects.filter(pk=pk, cfa=request.user, role=2).first()
        if not instance:
            return Response(
                data={"message": "Instructor not found"},
                status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(instance, data=request.data, context=context)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        context = {'request': request}
        instance = self.model.objects.filter(pk=pk, cfa=request.user, role=2).first()
        if not instance:
            return Response(
                data={"message": "Instructor not found"},
                status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(instance, data=request.data, partial=True, context=context)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        instance = self.model.objects.filter(pk=pk, cfa=request.user, role=2).first()
        if not instance:
            return Response(
                data={"message": "Instructor not found"},
                status=status.HTTP_404_NOT_FOUND)
        self.perform_destroy(instance)
        return Response(data={"message": "Instructor deleted"}, status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
