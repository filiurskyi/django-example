#!/bin/bash

# Start Celery worker in the background
celery -A quotes_proj worker --loglevel=INFO &

# Start Django development server
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
