#!/bin/bash

set -e

echo "Apply DB migrations..."
uv run python manage.py makemigrations
uv run python manage.py migrate

exec "$@"