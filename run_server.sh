#!/bin/sh

sleep 5

until python manage.py migrate
do
    echo "Waiting for db to be ready..."
done


python manage.py collectstatic --noinput;
gunicorn -w 2 -b 0:8000 backend.wsgi;
