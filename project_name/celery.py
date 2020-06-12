import os

from celery import Celery, signals
from configurations import importer
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{{ project_name }}.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", "Production")

app = Celery("{{ project_name }}")
app.config_from_object("django.conf:settings")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

importer.install()
