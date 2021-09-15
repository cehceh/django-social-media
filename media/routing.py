from django.urls import path

from . import consumers
 
websocket_urlpatterns = [
    path('ws/home/<int:pk>/', consumers.HomeConsumer.as_asgi()),
]