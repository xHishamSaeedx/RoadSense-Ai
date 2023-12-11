# celery.py (in your Django project directory or app directory)

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nohelmet_project.settings')

app = Celery('nohelmet_project')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS + ['webcam'])
from webcam.tasks import capture_frames

capture_frames()