REST API для получения данных из таблицы в Google Sheets
=====

Описание проекта
----------

Проект создан в рамках тестового задания для кандидатов-разработчиков. 

Проект состоит из проектируемого API сервиса для работы с данными клиентов и управления рассылками сообщений.

API сервис реализуется на базе фреймворка DRF.

[Ссылка на техническое задание]([https://www.craft.do/s/n6OVYFVUpq0o6L](https://kanalservis.notion.site/kanalservis/Python-82f517c516d041b8aca227f0a44ed1f1))

Системные требования
----------
* Python 3.6+
* Docker
* Works on Linux, Windows, macOS, BS

Стек технологий
----------
* Python 3.8
* Django 3.1
* Django Rest Framework
* PostreSQL
* Nginx
* gunicorn
* Docker
* Celery
* Redis

Установка проекта из репозитория (Linux и macOS)
----------
1. Клонировать репозиторий и перейти в него в командной строке:
```bash 
git clone git@github.com:NikitaChalykh/API_GoogleSheets_TW.git

cd API_GoogleSheets_TW
```

2. Cоздать и открыть файл ```.env``` с переменными окружения:
```bash 
cd infra

touch .env
```

3. Заполнить ```.env``` файл с переменными окружения по примеру:
```bash 
echo DB_ENGINE=django.db.backends.postgresql >> .env

echo DB_NAME=postgres >> .env

echo POSTGRES_PASSWORD=postgres >> .env

echo POSTGRES_USER=postgres >> .env

echo DB_HOST=db >> .env

echo DB_PORT=5432 >> .env

echo BROKER=redis://redis >> .env

echo BROKER_URL=redis://redis:6379/0 >> .env
```

4. Установка и запуск приложения в контейнерах:
```bash 
docker-compose up -d
```

5. Запуск миграций и сбор статики:
```bash 
docker-compose exec web python manage.py migrate

docker-compose exec web python manage.py collectstatic --no-input  
```
Документация к проекту
----------
Документация для API после установки доступна по адресу:

```http://127.0.0.1/redoc/```

```http://127.0.0.1/swagger/```
