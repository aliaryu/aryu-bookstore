FROM python:alpine

WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN python manage.py makemigrations
RUN python manage.py migrate

# THIS RUN 'filldb' SCRIPT TO FILL DATABASE
RUN python scripts/fill_database/filldb.py
