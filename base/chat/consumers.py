import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .models import Message
from .tasks import get_bot_message, send_bot_message

STOCK_PATTERN = '/stock='

class ChatConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def create_message(self, text_message, user, date, room_group):

        message = Message(
            user=user,
            text_message=text_message,
            date=date,
            room=room_group)
        message.save()

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

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

    async def receive(self, text_data):
        # Receive message from WebSocket
        text_data_json = json.loads(text_data)
        text_message = text_data_json['message']
        user = text_data_json['user']
        date = text_data_json['date']

        if STOCK_PATTERN not in text_message:
            await self.create_message(
                text_message,
                user,
                date,
                self.room_name)
        
            #Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': text_message,
                    'user': user,
                    'date': date,
                }
            )
        else:
            send_bot_message.delay(text_message, date, self.room_name)

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        user = event['user']
        date = event['date']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user' : user,
            'date': date,
        }))
