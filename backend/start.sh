#!/bin/bash

python manage.py makemigrations users
python manage.py migrate users
python manage.py migrate --noinput
python manage.py collectstatic --noinput
gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000
