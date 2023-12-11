from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from webcam_app.consumers import WebcamConsumer

websocket_urlpatterns = [
    path('ws/webcam/', WebcamConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    'websocket': URLRouter(websocket_urlpatterns),
})
