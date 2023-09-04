#!/bin/sh

until cd /app/
do
    echo "Waiting for server volume..."
done

celery -A backend worker --loglevel=info --concurrency 1 -E
