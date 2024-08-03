FROM python:3.9-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
RUN apk update \
    && apk add --no-cache gcc python3-dev postgresql-dev musl-dev \
    && pip install --no-cache-dir -r requirements.txt

COPY . /app
WORKDIR /app

RUN python manage.py collectstatic --noinput

COPY . /app
