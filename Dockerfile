FROM python:3.11-slim-buster

RUN apt-get update &&\
    apt-get upgrade -y &&\
    apt-get install -y libpq-dev gcc netcat-traditional
WORKDIR /app
RUN python -m pip install --upgrade pip
RUN pip install gunicorn
ADD backend/requirements.txt .
RUN pip install -r requirements.txt

ADD run_server.sh .
ADD run_worker.sh .
ADD run_worker_beat.sh .
RUN chmod +x run_server.sh
RUN chmod +x run_worker.sh
RUN chmod +x run_worker_beat.sh
ADD ./backend/ .
