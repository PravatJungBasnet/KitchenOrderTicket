#!/bin/bash
git pull origin main
workon venv
pip install -r requirements.txt --no-cache-dir
python manage.py migrate
python manage.py collectstatic --noinput
touch /var/www/pravat_pythonanywhere_com_wsgi.py
