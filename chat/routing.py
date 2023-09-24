from django.urls import path

from chat.consumers import NewMessageConsumer

websocket_urlpatterns = [
    path('ws/new-message/', NewMessageConsumer.as_asgi()),
]
