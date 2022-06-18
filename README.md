REST API для получения данных о заказах из Google Sheets
=====

Функциональные требования
----------
[Ссылка на техническое задание](https://kanalservis.notion.site/kanalservis/Python-82f517c516d041b8aca227f0a44ed1f1)

Описание проекта
----------
Проект создан в рамках тестового задания для кандидатов-разработчиков. 

Проект представляет собой API сервис для работы с данными о заказах товаров из таблицы в Google Sheets. 

API сервис реализуется на базе фреймворка DRF. 

В проекте применяется логирование, обработка исключений при доступе к внешним сетевым ресурсам, конфиденциальные данные хранятся в пространстве переменных окружения. Настроено отображение моделей проекта в панели администратора.

Реализован функционал проверки соблюдения «срока поставки» из таблицы. В случае, если срок поставки прошел, в Telegram отправляется уведомление. 

Данные для перевода $ в рубли рассчитываются по актуальному курсу ЦБ РФ с помощью XML котировок.

Задача коллекционирования и проверки данных из Google Sheets реализована в виде асинхронных Celery задач.

Проект разворачивается в следующих Docker контейнерах: web-приложение, postgresql-база данных, nginx-сервер, Redis-база данных и Celery-контейнер.

[Тестовая таблица Google Sheets с данными о заказах](https://docs.google.com/spreadsheets/d/1OpCylqw4U-64lMKZFVk7fhllqOvczTD5eb516aDghbo/edit#gid=0) 

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
* Telegram Bot API
* BeautifulSoup4

Установка проекта из репозитория (Linux и macOS)
----------
1. Клонировать репозиторий и перейти в него в командной строке:
```bash 
git clone git@github.com:NikitaChalykh/API_GoogleSheets_TW.git

cd API_GoogleSheets_TW
```

2. Скопировать файл ```credentials.json```(передан в чате "HR-бот Каналсервис" отдельным файлом) в корневую папку backend рядом с файлом ```manage.py```

3. Cоздать и открыть файл ```.env``` с переменными окружения:
```bash 
cd ../infra

touch .env
```

4. Заполнить ```.env``` файл с переменными окружения по примеру:
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
* ID телеграм чата для получения уведомлений
```bash
echo CHAT_ID=**************** >> .env
```

5. Установка и запуск приложения в контейнерах:
```bash
docker-compose up -d
```

6. Запуск миграций, сбор статики, создание суперпользователя:
```bash 
docker-compose exec web python manage.py migrate

docker-compose exec web python manage.py collectstatic --no-input  

docker-compose exec web python manage.py createsuperuser
```
Документация к проекту
----------
Документация для API после установки доступна по адресу:

```http://127.0.0.1/redoc/```

```http://127.0.0.1/swagger/```
