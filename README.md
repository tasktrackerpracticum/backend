![workflow status](https://github.com/tasktrackerpracticum/backend/actions/workflows/taksa-tracker.yml/badge.svg)
# Taksa Tracker backend

## Проект доступен по адресу

 https://taksa-tracker.ru
 
 https://taksa-tracker.ru/api/docs/
 
<details>

<summary>Запуск проекта локально</summary>

## Запуск в докере

```
git clone git@github.com:tasktrackerpracticum/backend.git
cd backend
docker build -t tasktracker .
docker run -it -p 8000:8000 tasktracker
```

## Запуск локально

1. Установить [Python](https://www.python.org/downloads/release/python-3107/).

2. Скопировать репозиторий и создать окружение.
```
git clone git@github.com:tasktrackerpracticum/backend.git
cd backend
make setup
```

3. Запустить сервер:

```
make run
```
4. Открыть в браузере.
   
http://localhost:8000/api/docs/

## Админка

http://localhost:8000/admin/

Логин admin@admin.com
Пароль admin

## Документация

http://localhost:8000/api/docs

Требует авторизации (кнопка authorize)

Bearer {token}

Также работает авторизация Django - нажать кнопку Django Login

### Токен

Выдаёт конечная точка http://localhost:8000/jwt/create/

```
{

"email": "admin@admin.com",
"password": "admin"

}

<details>
```
## Сделать дамп базы на Windows

```

python -Xutf8 manage.py dumpdata --exclude auth.permission --exclude contenttypes --indent 2 > db.json

```
