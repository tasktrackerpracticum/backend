# Tracker

## Пререквизиты

Необходим python.

Можно скачать https://www.python.org/downloads/release/python-3107/

## Запуск

git clone https://github.com/Konstantin8891/Tracker.git

cd backend

Windows:

python -m venv venv

source venv/Scripts/activate

Mac, Linux:

python3 -m venv venv

. venv/bin/activate

Далее:

pip install -r requirements.txt

python manage.py runserver

## Документация

http://localhost:8000/api/docs

Требует авторизации (кнопка authorize)

Bearer {token}

### Токен

Выдаёт конечная точка jwt/create

{

"email": "admin@admin.com",

"password": "admin"

}
