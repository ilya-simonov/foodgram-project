Проект доступен по адресу - http://158.160.19.152/

![example workflow](https://github.com/carden-code/foodgram-project-react/actions/workflows/main.yml/badge.svg)

### Проект доступен по адресу - http://158.160.19.152/

# Foodgram, «Продуктовый помощник»
 Проект Foodgram позволяет пользователем публиковать свои рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.


## Как запустить проект, используя Docker (база данных PostgreSQl):
Клонировать репозиторий и перейти в него в командной строке:
```bash
    git clone git@github.com:ilya-simonov/foodgram-project.git
    cd foodgram-project
```

- Пример заполнения файла .env:

```DB_ENGINE=django.db.backends.postgresql # указываем, что работаем c postgresql

   DB_NAME=postgres # имя базы данных

   POSTGRES_USER=postgres # логин для подключения к базе данных

   POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)

   DB_HOST=db # название сервиса (контейнера)

   DB_PORT=5432 # порт для подключения к БД

   SECRET_KEY=ваш секретный ключ
```

- Cборка docker-compose:

```bash
    cd infra
    docker-compose up -d --build 
```
- Выполните по очереди команды:

```bash
    docker-compose exec backend python manage.py makemigrations
    docker-compose exec backend python manage.py migrate
    docker-compose exec backend python manage.py load_ingredients
    docker-compose exec backend python manage.py createsuperuser
    docker-compose exec backend python manage.py collectstatic --no-input 
```

- Зайдите в админку и создайте Tags:

```bash
    http://localhost/admin
```
____
Ваш проект запустился на http://localhost/

### Автор:

#### [Илья Симонов](https://github.com/ilya-simonov "Ilya Simonov")
