"""
ASGI config for webcam_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter
from webcam_project.routing import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webcam_project.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(websocket_urlpatterns),
    # ... other protocols
})