"""
Compat shim so gunicorn oliveoshoppe.wsgi:application still works after moving wsgi to project root.
"""
from importlib import import_module

application = import_module('wsgi').application
