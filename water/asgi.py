import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from django.core.asgi import get_asgi_application

import media.routing
import chat.routing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'water.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            media.routing.websocket_urlpatterns + 
            chat.routing.websocket_urlpatterns
        )
    )
})
