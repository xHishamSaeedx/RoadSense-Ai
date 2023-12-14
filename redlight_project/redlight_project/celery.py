# celery.py (in your Django project directory or app directory)
from __future__ import absolute_import, unicode_literals
from celery import Celery
import os
from django.conf import settings
import multiprocessing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'redlight_project.settings')

app = Celery('redlight_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
from webcam.tasks import capture_frames
from wrong_side.tasks import capture_frames2
from nohelmetapp.tasks import capture_frames3

capture_frames2()

# # #Create processes for each function
# process1 = multiprocessing.Process(target=capture_frames)
# # process2 = multiprocessing.Process(target=capture_frames2)
# process3 = multiprocessing.Process(target=capture_frames3)

# # # Start both processes
# process1.start()
# # process2.start()
# process3.start()
# # # Wait for both processes to finish
# process1.join()
# # process2.join()
# process3.join()