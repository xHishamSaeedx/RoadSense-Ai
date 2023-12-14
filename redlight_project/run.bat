start "Django Server" cmd /k python manage.py runserver
start "Celery Worker" cmd /k celery -A redlight_project.celery worker --pool=solo -l info  
