from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter

from django.core.asgi import get_asgi_application

import os

import chat.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DrygaChat.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    "websocket": URLRouter(chat.routing.websocket_urlpatterns),
})
