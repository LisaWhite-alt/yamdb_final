[![Django-app workflow](https://github.com/LisaWhite-alt/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)](https://github.com/LisaWhite-alt/yamdb_final/actions/workflows/yamdb_workflow.yml)


# yamdb_final

## Описание проекта

С помощью облачного сервиса GitHub Actions автоматизируются действия
по разворачиванию, тестированию, синхроназации приложения api_yamdb
на боевом сервере с последующим уведомленим об успешности действий
через бота Telegram и бейджа в Readme

### Технологии

* Docker
* Docker-compose
* Python 3.8.5
* Django 3.0.5

### Инструкция по установке Docker и Docker-compose на сервер

`sudo apt install docker.io`
[Ссылка:](https://docs.docker.com/compose/install/)

### Проект берем отсюда

[Ссылка:](https://github.com/LisaWhite-alt/yamdb_final.git)

### Добавить в Secrets GitHub Actions переменные окружения

```python
DB_ENGINE
DB_HOST
DB_NAME
DB_PORT
DOCKER_PASSWORD
DOCKER_USERNAME
HOST
PASSPHRASE
POSTGRES_PASSWORD
POSTGRES_USER
SSH_KEY
TELEGRAM_TO
TELEGRAM_TOKEN
USER
```

### Поместить на сервер:

docker-compose.yaml
/nginx
/static

### Команда для запуска

push в репозиторий в ветки master или main

### Сделать миграции

```python
docker-compose exec web python manage.py migrate auth
docker-compose exec web python manage.py migrate --run-syncdb
```

### Команда для создания суперпользователя

`winpty docker-compose exec web python manage.py createsuperuser`

### Собрать статику

`docker-compose exec web python manage.py collectstatic --no-input`

### Заполнение базы данных

Через админку Django

### Адрес для проверки работоспособности

[Ссылка:](http://lisatube.co.vu/redoc)

### Автор

Богомолова Екатерина