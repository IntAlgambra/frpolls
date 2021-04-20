# Candyapi

Реализация тестового задания от Фабрики Решений. API для управления опросами

## Требования

1. Docker

2. docker-compose

## Инструкции по деплою

1. Клонируем репозиторий

```
git clone https://github.com/IntAlgambra/frpolls.git
```

2. Переходим в папку проекта и создаем файл с переменными окружения .frtest.env


3. Прописываем в .frtest.env необходимые переменные окружения

```
DJANGO_SECRET_KEY=секретный ключ приложения Джанго
POSTGRES_USER=имя пользователя в БД Postgres
POSTGRES_PASSWORD=пароль пользователя в БД Postgres

```

4. Запускаем приложение  и производим миграции БД

```
sudo docker-compose up -d --build
sudo docker-compose run --rm backend python manage.py migrate
```

5. Добавляем суперпользователя для управления опросами


## Обновление приложения

1. Подтягиваем новую версию приложения из удаленного репозитория

```
git pull
```

2. Пересобираем контейнеры и запускаем миграции БД

```
sudo docker-compose up -d --build
sudo docker-compose run --rm backend python manage.py migrate
```

## Авторизация

В приложении реализована простейшая авторизация с помощью jwt-токенов. В ответе на логин
клиент получает токен доступа, который необходимо устанавливать в заголовк авторизации
при каждом защищенном запросе

```
Authorizationn: Bearer {token}
```

## Документация

Документация в формате openapi находится в файле openapi.yml