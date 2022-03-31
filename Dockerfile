FROM python:3.9-slim-buster

WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY . /app

RUN apt-get update && apt-get install python3-dev default-libmysqlclient-dev build-essential -y
RUN pip install --upgrade pip && pip install -r requirements.txt