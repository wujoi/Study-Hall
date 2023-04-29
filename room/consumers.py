import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User

from .models import Message, Room

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['slug']
        self.room_group_name = 'chat_%s' % self.room_name
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        chatmessage = data['chatmessage']
        username = data['username']
        room = data['room']

        await self.save_message(username, room, chatmessage)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'chatmessage': chatmessage,
                'username': username,
                'room': room,
            }
        )
        
    async def chat_message(self, event):
        chatmessage = event['chatmessage']
        username = event['username']
        room = event['room']

        await self.send(text_data=json.dumps({
            'chatmessage': chatmessage,
            'username': username,
            'room': room,
        }))
    
    @sync_to_async
    def save_message(self, username, room, chatmessage):
        user = User.objects.get(username=username)
        room = Room.objects.get(slug=room)
        
        Message.objects.create(user=user, room=room, content=chatmessage)

class UserActivityConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'user_activity'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def user_activity_update(self, event):
        active_users = event['active_users']
        away_users = event['away_users']
        inactive_users = event['inactive_users']

        await self.send(text_data=json.dumps({
            'type': 'user_activity_update',
            'active_users': active_users,
            'away_users': away_users,
            'inactive_users': inactive_users
        }))

