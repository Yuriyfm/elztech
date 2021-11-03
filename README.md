# elztech
RESTful API сервер на django и django rest framework. БД - postgresql.

### Для запуска приложения:

Внесите в файл .env свои данные подключения к БД (подгружаются в проект как переменные окружения)

Для создания БД запустить файл utils/create_db.py

Произвести миграции для создания таблиц

    python manage.py makemigrations authentication
    python manage.py makemigrations complexes
    python manage.py migrate
    
Для наполнения таблицы complexes данными запустить файл utils/upload_complex_data.py

запуск приложения 

    python manage.py runserver
    
приложение будте доступно по адресу - http://127.0.0.1:8000

### Маршруты и примеры JSON находятся в корне проекта в файле - enpoints and jsons examples.txt 
