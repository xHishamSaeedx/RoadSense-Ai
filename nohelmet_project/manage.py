#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from subprocess import Popen
import shlex



def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nohelmet_project.settings")
    try:
        command = 'celery -A nohelmet_project worker -l info'
        Popen(shlex.split(command))

        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

    # if 'runserver' in sys.argv:
    #     command = 'celery -A nohelmet_project worker -l info'
    #     Popen(shlex.split(command))


if __name__ == "__main__":
    main()
