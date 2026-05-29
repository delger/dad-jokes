"""WSGI config for dad_jokes_project."""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dad_jokes_project.settings")

application = get_wsgi_application()
