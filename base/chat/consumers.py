import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .models import Message
from .tasks import get_bot_message, send_bot_message

class ChatConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def create_message(self, text_message):

        message = Message(
            user=self.scope['user'],
            text_message=text_message)
        message.save()

    async def connect(self):
        self.room_group_name = 'chat_room'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        text_message = text_data_json['message']

        await self.create_message(text_message)
        
        #Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': text_message
            }
        )

        send_bot_message.delay(text_message)

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
