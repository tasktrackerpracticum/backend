FROM python:3.11-slim-buster

RUN apt-get update &&\
    apt-get upgrade -y &&\
    apt-get install -y libpq-dev gcc netcat-traditional
RUN python -m pip install --upgrade pip
WORKDIR /app
COPY run.sh .
COPY backend/requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir && pip install gunicorn
COPY ./backend/ .
RUN chmod +x run.sh
ENTRYPOINT ["/app/run.sh"]
