#!/bin/sh
sleep 5
python manage.py migrate;
python manage.py collectstatic --noinput;
gunicorn -w 2 -b 0:8000 backend.wsgi;
