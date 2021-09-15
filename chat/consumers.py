import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from .models import *



class NormalChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = int(self.scope['url_route']['kwargs']['pk'])
        self.partner = int(self.scope['url_route']['kwargs']['partner'])
        self.room_name = self.user + self.partner
        self.room_group_name = 'chat_%d' % self.room_name
        # Join room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
    
    async def disconnect(self, close_code):
        # Leave room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    # Receive message from web socket
    async def receive(self, text_data):

        data = json.loads(text_data)
        message = data.get('message') if data.get('message') else None
        online = data.get('online') if data.get('online') else None
        typing = data.get('typing') if data.get('typing') else None
        delete = data.get('delete') if data.get('delete') else None

        
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'online': online,
                'typing': typing,
                'delete': delete,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event.get('message') if event.get('message') else None
        online = event.get('online') if event.get('online') else None
        typing = event.get('typing') if event.get('typing') else None
        delete = event.get('delete') if event.get('delete') else None

        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'online': online,
            'typing': typing,
            'delete': delete,
        }))
