FROM python:3.9-alpine



ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY . /app
WORKDIR /app

RUN apk update \
    && apk add gcc python3-dev postgresql-dev

RUN pip3 install -r requirements.txt

RUN python manage.py collectstatic --noinput

RUN python manage.py makemigrations
RUN python manage.py migrate

