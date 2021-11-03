from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from complexes.serializers import ComplexSerializer, ComplexDeleteSerializer, \
    ComplexUpdateSerializer, ComplexCreateSerializer, GetComplexSerializer
from complexes.models import Complex
from rest_framework.permissions import IsAuthenticated
import uuid


class GetComplexesList(ListAPIView):
    """ Возвращает все записи из таблицы Complexes"""

    queryset = Complex.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ComplexSerializer


class GetComplex(APIView):
    """Возвращает данные конкретного Комплекса"""

    queryset = Complex.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = GetComplexSerializer

    def get(self, request):
        data = request.data
        serializer = self.serializer_class(data=data['complex'])
        serializer.is_valid(raise_exception=True)
        complex_id = serializer.validated_data['id']
        the_complex = Complex.objects.get(id=complex_id)
        serializer = ComplexSerializer(the_complex)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateComplex(CreateAPIView):
    """принимает данные комплекса и создает новую запись в таблице complexes"""

    queryset = Complex.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ComplexCreateSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data['complex'])
        serializer.is_valid(raise_exception=True)
        complex_name = serializer.validated_data['name']
        new_complex = Complex.objects.create(name=complex_name)
        new_complex.save()
        return Response({'response': f'new complex created successfully'}, status=status.HTTP_200_OK)


class UpdateComplex(UpdateAPIView):
    """принимает id и имя комплекса и обновляет имя в БД с созданием нового uuid"""

    queryset = Complex.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ComplexUpdateSerializer

    def update(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data['complex'])
        serializer.is_valid(raise_exception=True)
        complex_id = serializer.validated_data['id']
        complex_name = serializer.validated_data['name']
        instance = self.queryset.get(pk=complex_id)
        instance.name = complex_name
        instance.uuid = uuid.uuid4()
        instance.save()
        return Response({'response': f'complex with id = {complex_id} updated successfully'}, status=status.HTTP_200_OK)


class DeleteComplex(DestroyAPIView):
    """принимает id комплекса и удаляет его"""

    queryset = Complex.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ComplexDeleteSerializer

    def delete(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data['complex'])
        serializer.is_valid(raise_exception=True)
        complex_id = serializer.validated_data['id']
        instance = self.queryset.get(pk=complex_id)
        instance.delete()
        return Response({'response': f'complex with id = {complex_id} deleted successfully'}, status=status.HTTP_200_OK)
