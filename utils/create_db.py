import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv


load_dotenv()
# Модуль для создания новой базы перед первым запуском


def create_db(name, password, user):
    """Функция принимает на вход данные подключения к БД из config.ini и создает новую БД"""
    try:
        # Устанавливаем соединение с postgres
        connection = psycopg2.connect(user=user, password=password)
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        # Создаем курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        # Создаем базу данных
        sql_create_database = cursor.execute(f'create database {name}')
        # Закрываем соединение
        cursor.close()
        connection.close()
        return f'База данных {os.getenv("DB_NAME")} успешно создана'
    # ловим ошибку если БД с таким именем уже существует
    except psycopg2.errors.DuplicateDatabase:
        return'База данных с таким именем уже существует'
    # ловим ошибку если указан неверный пользователь или пароль
    except psycopg2.OperationalError:
        return'Указан неверный db_user или db_password'


print(create_db(os.getenv('DB_NAME'), os.getenv('DB_PASSWORD'), os.getenv('DB_USER')))
