![workflow status](https://github.com/tasktrackerpracticum/backend/actions/workflows/taksa-tracker.yml/badge.svg)
# Tracker

## Проект доступен по адресу

 https://taksa-tracker.ru

## Запуск в докере

```
git clone git@github.com:tasktrackerpracticum/backend.git
cd backend
docker build -t tasktracker .
docker run -it -p 8000:8000 tasktracker
```

## Запуск локально

Необходим python.

Можно скачать https://www.python.org/downloads/release/python-3107/

```
git clone git@github.com:tasktrackerpracticum/backend.git
cd backend
make setup
```

Запустить сервер:

```
make run
```

## Админка

http://localhost:8000/admin/

Логин admin@admin.com
Пароль admin

## Документация

http://localhost:8000/api/docs

Требует авторизации (кнопка authorize)

Bearer {token}

Также работает авторизация Django - нажать кнопку Django Login (только пока тестовый режим)

### Токен

Выдаёт конечная точка http://localhost:8000/jwt/create/

```
{

"email": "admin@admin.com",
"password": "admin"

}
```
## Сделать дамп базы на Windows

```

python -Xutf8 manage.py dumpdata --exclude auth.permission --exclude contenttypes --indent 2 > db.json

```
