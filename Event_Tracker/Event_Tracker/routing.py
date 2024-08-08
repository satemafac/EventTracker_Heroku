# routing.py

from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from event import consumers

websocket_urlpatterns = [
    path('ws/transcribe/', consumers.TranscribeConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    'websocket': URLRouter(websocket_urlpatterns),
})
