# Tracker

## Пререквизиты

Необходим python.

Можно скачать https://www.python.org/downloads/release/python-3107/

## Запуск

```
git clone https://github.com/Konstantin8891/Tracker.git

cd backend
```

Windows:

```
python -m venv venv

source venv/Scripts/activate
```

Mac, Linux:

```
python3 -m venv venv

. venv/bin/activate
```

Далее:

```
pip install -r requirements.txt

python manage.py migrate

python manage.py loaddata db.json

python manage.py runserver

```

## Документация

http://localhost:8000/api/docs

Требует авторизации (кнопка authorize)

Bearer {token}

Также работает авторизация Django - нажать кнопку Django Login

### Токен

Выдаёт конечная точка jwt/create

```
{

"email": "admin@admin.com",

"password": "admin"

}
```

###  Второй вариант авторизации (только для тестового режима)

перейти по адресу: http://localhost:8000/admin
авторизоваться по email: admin@admin.com
пароль: admin

## Сделать дамп базы на Windows

```

python -Xutf8 manage.py dumpdata --exclude auth.permission --exclude contenttypes --indent 2 > db.json

```
