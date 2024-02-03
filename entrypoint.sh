#!/bin/bash

echo "Apply DB migration"
python manage.py makemigrations
python manage.py migrate
exec "$@"