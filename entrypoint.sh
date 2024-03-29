#!/bin/sh

python manage.py makemigrations
python manage.py migrate
python .\scripts\fill_database\filldb.py

exec "$@"
