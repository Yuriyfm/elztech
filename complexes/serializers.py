from rest_framework import serializers
from complexes.models import Complex
from rest_framework import status
from rest_framework.response import Response

class ComplexSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complex
        fields = '__all__'


class ComplexDetailSerializer(serializers.ModelSerializer):
    """Сериализует и возвращает данные конкретного пользователя и данные relation моделей"""

    class Meta:
        model = Complex
        fields = '__all__'


class ComplexCreateSerializer(serializers.ModelSerializer):
    """Проводит валидацию name"""

    name = serializers.CharField(max_length=150, write_only=True)

    class Meta:
        model = Complex
        fields = ['name']

    def validate(self, data):
        name = data.get('name', None)

        if name is None:
            raise serializers.ValidationError(Response(
                {'response': 'An name is required to delete.'}, status=status.HTTP_204_NO_CONTENT))

        validation_data = {'name': name}

        return validation_data


class ComplexUpdateSerializer(serializers.ModelSerializer):
    """Проводит валидацию id и name и проверяет наличие записи с указанным id в БД"""

    id = serializers.CharField(max_length=255, write_only=True)
    name = serializers.CharField(max_length=150, write_only=True)

    class Meta:
        model = Complex
        fields = ['id', 'name']

    def validate(self, data):
        id = data.get('id', None)
        name = data.get('name', None)

        if id is None:
            raise serializers.ValidationError(
                'An id is required to delete.')
        if id.isdigit() == False:
            raise serializers.ValidationError(
                'id value must be integer.')
        try:
            Complex.objects.get(pk=id)
        except Complex.DoesNotExist:
            raise serializers.ValidationError(
                'id not in database.')
        if name is None:
            raise serializers.ValidationError(
                'An name is required to delete.')
        validated_data = {'id': id, 'name': name}

        return validated_data


class ComplexDeleteSerializer(serializers.ModelSerializer):
    """Проводит валидацию id и проверяет его наличие в БД"""

    id = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = Complex
        fields = ['id']

    def validate(self, data):
        id = data.get('id', None)
        if id is None:
            raise serializers.ValidationError(
                'An id is required to delete.')
        if id.isdigit() == False:
            raise serializers.ValidationError(
                'id value must be integer.')
        try:
            Complex.objects.get(pk=id)
        except Complex.DoesNotExist:
            raise serializers.ValidationError(
                'id not in database.')
        validated_data = {'id': id}
        return validated_data


class GetComplexSerializer(serializers.ModelSerializer):
    """Проводит валидацию id и проверяет его наличие в БД"""

    id = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = Complex
        fields = ['id']

    def validate(self, data):
        id = data.get('id', None)
        if id is None:
            raise serializers.ValidationError(
                'An id is required to get complex.')
        if id.isdigit() == False:
            raise serializers.ValidationError(
                'id value must be integer.')
        try:
            Complex.objects.get(pk=id)
        except Complex.DoesNotExist:
            raise serializers.ValidationError(
                'id not in database.')
        validated_data = {'id': id}
        return validated_data
