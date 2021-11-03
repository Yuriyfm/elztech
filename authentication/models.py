from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from complexes.models import Complex
from rest_framework.authtoken.models import Token


class UserManager(BaseUserManager):
    """ manager модели User с методами создания обычного пользователя и суперпользователя """

    def create_user(self, username, first_name, last_name, patronymic,  password):
        """ Создает пользователя с паролем и именем """

        if username is None:
            raise TypeError('Поле username является обязательным')
        user = self.model(username=username, first_name=first_name, last_name=last_name, patronymic=patronymic)
        user.set_password(password)
        user.save()
        token = Token.objects.create(user=user)
        return user

    def create_superuser(self, username, password):
        """ Создает и возввращет пользователя с привилегиями суперадмина. """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ Модель сущности User"""

    username = models.CharField(db_index=True, max_length=255, unique=True, verbose_name='Логин')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150,  verbose_name='Фамилия')
    patronymic = models.CharField(max_length=150, verbose_name='Отчество')
    user_role = models.IntegerField(default=1, verbose_name='Роль')
    complex = models.ForeignKey(Complex, default=1, verbose_name='Комплекс', on_delete=models.PROTECT)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    # указываем менеджер для модели
    objects = UserManager()

    def __str__(self):
        return self.username

    def get_full_name(self):
        return f"{self.last_name} {self.first_name} {self.patronymic}"

    def get_short_name(self):
        return self.username

