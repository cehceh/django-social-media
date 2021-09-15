from django.urls import path

from .consumers import NormalChatConsumer

websocket_urlpatterns = [
    path('ws/<str:pk>/<str:partner>/', NormalChatConsumer.as_asgi()),
]
