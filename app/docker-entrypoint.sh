#!/bin/sh
set -e

echo 'Run Migration...'
python manage.py migrate --noinput

echo 'Creating superuser...'
python manage.py createsuperuser_if_none_exists --user=admin --password=admin

exec "$@"