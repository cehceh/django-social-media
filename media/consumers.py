import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import User

@sync_to_async
def ConnetUser(pk):
    user = User.objects.get(pk=pk)
    user.is_online = True
    user.save()

@sync_to_async
def DisConnetUser(pk):
    user = User.objects.get(pk=pk)
    user.is_online = False
    user.save()


class HomeConsumer(AsyncWebsocketConsumer, object):


    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['pk']
        self.notify_group_name = 'notify_%d'% self.user_id 
        if self.scope['user'].id != self.user_id:
            await self.close()
        # Join room
        await self.channel_layer.group_add(
            self.notify_group_name,
            self.channel_name
        )

        await self.accept()

        

        await ConnetUser(self.user_id)



    async def disconnect(self, close_code):
        # Leave room
        await self.channel_layer.group_discard(
            self.notify_group_name,
            self.channel_name
        )

        await DisConnetUser(self.user_id)

    async def chat_message(self, event):
        notify = event.get("notify" or None)
        request_pk = event.get("request_pk" or None)
        notify_delete = event.get("notify_delete" or None)
        request_delete = event.get("request_delete" or None)
        message = event.get("messages" or None)
        # Send message to WebSocket
        await self.send(text_data=json.dumps({'notify': notify, 'request_pk': request_pk, 'notify_delete':notify_delete, "request_delete":request_delete, 'message': message,}))

    
