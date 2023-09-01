#!/bin/sh

until cd /app/
do
    echo "Waiting server volume..."
done


until python manage.py migrate
    echo "Waiting for db to be ready..."
done


python manage.py collectstatic --noinput;
gunicorn -w 2 -b 0:8000 backend.wsgi;
