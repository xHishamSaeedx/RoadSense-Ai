# celery.py (in your Django project directory or app directory)
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
import multiprocessing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'redlight_project.settings')

app = Celery('redlight_project')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS + ['webcam'] + ['wrong_side'])
from webcam.tasks import capture_frames
from wrong_side.tasks import capture_frames2

# Create processes for each function
process1 = multiprocessing.Process(target=capture_frames)
process2 = multiprocessing.Process(target=capture_frames2)

# Start both processes
process1.start()
process2.start()

# Wait for both processes to finish
process1.join()
process2.join()