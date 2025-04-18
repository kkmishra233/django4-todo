#!/bin/bash

set -e

echo "Apply DB migrations..."
uv run python manage.py makemigrations
uv run python manage.py migrate

echo "Starting Django server..."
exec uv run python manage.py runserver 0.0.0.0:8080