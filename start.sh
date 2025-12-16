#!/bin/bash
set -e

echo "=== Starting Oliveoshoppe ==="
echo "Python version:"
python --version

echo "=== Running Database Migrations ==="
python manage.py migrate --noinput || echo "Migrations failed, continuing..."

echo "=== Creating Admin Users ==="
python manage.py create_admins

echo "=== Loading Products ==="
python manage.py load_products

echo "=== Starting Gunicorn ==="
exec gunicorn oliveoshoppe.wsgi:application --bind 0.0.0.0:10000
