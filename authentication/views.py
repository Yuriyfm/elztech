from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import LoginSerializer, RegistrationSerializer, UsersListSerializer, UserDetailSerializer, \
    UserSerializer


class RegistrationAPIView(APIView):
    """Обработчик запросов для регистрации нового пользователя. Принимает в POST запросе данные нового пользователя,
    передает их в сериалайзер для валидации и сериализации и возвращает сообщение об успешном добавлении"""

    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'response': f'Registration new user {serializer.data["username"]} completed successfully'},
                        status=status.HTTP_200_OK)


class LoginAPIView(APIView):
    """Обработчик запросов для авторизации пользователя. Принимает в POST запросе данные для авторизации
    передает их в сериалайзер для валидации и возвращает токен"""

    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class GetUsersListApi(ListAPIView):
    """Возвращает список всех юзеров"""

    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UsersListSerializer


class GetUserDetailApi(APIView):
    """Возвращает данные конкретного юзера"""

    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UserDetailSerializer

    def get(self, request):
        data = request.data
        serializer = self.serializer_class(data=data['user'])
        serializer.is_valid(raise_exception=True)
        user_id = serializer.validated_data['id']
        user = User.objects.get(id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


