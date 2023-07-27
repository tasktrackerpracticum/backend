FROM python:3.11-slim

RUN apt-get update && apt-get upgrade -y && apt-get install -y libpq-dev gcc && pip install psycopg2
WORKDIR /app
COPY run.sh .
COPY ./backend/ .
RUN pip install -U pip && pip install -r requirements.txt --no-cache-dir && pip install gunicorn
RUN chmod +x run.sh
ENTRYPOINT ["/app/run.sh"]
