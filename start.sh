#!/bin/bash
set -e

echo "=== Starting Oliveoshoppe ==="
echo "Python version:"
python --version

echo "=== Running Database Migrations ==="
python manage.py migrate --noinput || echo "Migrations failed, continuing..."

echo "=== Starting Gunicorn ==="
exec gunicorn oliveoshoppe.wsgi:application --bind 0.0.0.0:10000
