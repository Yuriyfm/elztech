from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    """ Сериализация регистрации и создания нового пользователя. """

    # пароль должен содержать не менее 8 символов, не более 128
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'patronymic']

    def create(self, validated_data):
        # Используем метод create_user из модели User
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    """ Принимает логин и пароль, проводит их валидацию проверяет наличие пользователя с такими данными в БД.
    Если пользователь найден возвращает токен"""

    username = serializers.CharField(max_length=255, write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        # проверяем наличие в входящих данных username и password
        username = data.get('username', None)
        password = data.get('password', None)
        # Вызвать исключение, если не предоставлен пароль
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
        # Вызвать исключение, если не предоставлен username
        if username is None:
            raise serializers.ValidationError(
                'An username is required to log in.'
            )
        # Метод authenticate выполняет проверку, что почта и пароль соответствуют юзеру из БД
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this username and password was not found.'
            )

        # проверяем флаг is_active
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )
        # возвращаем токен
        token = user.auth_token
        return {
            'token': token
        }


class UsersListSerializer(serializers.ModelSerializer):
    """Сериализует и возвращает список всех пользователей"""

    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'patronymic', 'username', 'user_role', 'complex')


class UserDetailSerializer(serializers.ModelSerializer):
    """Сериализует и возвращает данные конкретного пользователя и данные relation моделей"""

    id = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        depth = 1
        fields = ('id',)

    def validate(self, data):
        user_id = data.get('id', None)
        if user_id is None:
            raise serializers.ValidationError(
                'An id is required to get user detail.')
        if not user_id.isdigit():
            raise serializers.ValidationError(
                'id value must be integer.')
        try:
            User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'id not in database.')
        validated_data = {'id': user_id}
        return validated_data


class UserSerializer(serializers.ModelSerializer):
    """Сериализует данные объекта user"""

    class Meta:
        model = User
        depth = 1
        fields = ('last_name', 'first_name', 'patronymic', 'username', 'user_role', 'complex')
