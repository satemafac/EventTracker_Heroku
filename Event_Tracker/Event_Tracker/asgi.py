import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import Event_Tracker.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Event_Tracker.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(Event_Tracker.routing.websocket_urlpatterns),
})
