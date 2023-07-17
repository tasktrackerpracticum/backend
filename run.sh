#!/bin/sh
python manage.py migrate;
python manage.py collectstatic --noinput;
python manage.py loaddata db.json
gunicorn -w 2 -b 0:8000 backend.wsgi;
