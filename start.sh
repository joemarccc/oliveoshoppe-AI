#!/bin/bash
set -e

echo "=== Running Database Migrations ==="
python manage.py migrate --noinput

echo "=== Starting Gunicorn ==="
gunicorn oliveoshoppe.wsgi:application
