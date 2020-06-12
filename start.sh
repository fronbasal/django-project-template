#!/usr/bin/env bash
set -e

if [[ $* == *--migrate* ]]; then
  echo '[APP] Migrating database'
  python manage.py migrate
fi

if [[ $* == *--run* ]]; then
    echo '[APP] Running migrate'
    python3 manage.py migrate -v 0 --run-syncdb
    echo '[APP] Running collectstatic'
    python3 manage.py collectstatic -v 0 --clear --noinput
    echo '[APP] Running server'
    uwsgi --env DJANGO_SETTINGS_MODULE={{ project_name }}.settings --env DJANGO_SECRET_KEY="${DJANGO_SECRET_KEY}" --master --http=0.0.0.0:8000 --processes 4 --enable-threads --env DJANGO_CONFIGURATION=Production --module={{ project_name }}.wsgi:application
fi

if [[ $# -eq 0 ]]; then
    echo "[APP] No arguments given"
    exit 1
fi
