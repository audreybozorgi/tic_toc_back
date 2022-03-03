from channels.routing import ProtocolTypeRouter
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/game-status', consumers.GameStatusConsumer.as_asgi()),
]