from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('wss/chat/<str:room_name>/', consumers.ChatConsumer.as_asgi()),
    path('wss/home/', consumers.LoginStatusConsumer.as_asgi()),
]