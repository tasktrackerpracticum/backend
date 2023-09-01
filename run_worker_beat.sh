#!/bin/sh

until cd /app/
do
    echo "Waiting for server volume..."
done

celery -A backend beat --loglevel=info
