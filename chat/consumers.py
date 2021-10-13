from channels.generic.websocket import AsyncWebsocketConsumer, AsyncJsonWebsocketConsumer
from django.template.loader import render_to_string
from channels.db import database_sync_to_async
from django.core.serializers import serialize
from asgiref.sync import sync_to_async
from .models import *
import json
from django.http import JsonResponse
from django.contrib.auth.models import User


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('Connected')
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        print('Disconnected')

        # Leave room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from web socket
    async def receive(self, text_data):

        # Retrieve data sent from socket.send() method in JavaScript
        # of associated template
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        room = data['room']

        await self.save_message(username, room, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'date_added': await self.get_message_date_added(username, message)
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'date_added': await self.get_message_date_added(username, message)
        }))

    @sync_to_async
    def save_message(self, username, room, message):
        # Message.objects.create(username=username, room=Room.objects.get(
        #     name=room), content=message)

        Message.objects.create(user=User.objects.get(username=username), room=Room.objects.get(
            name=room), content=message)

    @sync_to_async
    def get_message_date_added(self, username, message):
        # Serializer waits for normal queryset, not ValuesQuerySet (which is returned by values).
        # If you want to query only certain fileds, use only.
        # date_added = Message.objects.filter(content=message,
        #                                     username=username)

        date_added = Message.objects.filter(content=message,
                                            user=User.objects.get(username=username))

        # return JsonResponse({'date_added': list(date_added)})
        return json.loads(serialize('json', date_added))[0]['fields']['date_added']


class LoginStatusConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("users", self.channel_name)

        user = self.scope['user']

        if user.is_authenticated:
            await self.update_user_status(user, True)
            await self.send_status()

    async def disconnect(self, code):
        await self.channel_layer.group_discard("users", self.channel_name)
        user = self.scope['user']

        if user.is_authenticated:
            await self.update_user_status(user, False)
            await self.send_status()

    async def send_status(self):
        # Take Profile of all users
        users = Profile.objects.all()

        # Send message to WebSocket
        await self.channel_layer.group_send(
            'users',
            {
                "type": "user_update",
                "event": "Change Status",
                # Send template for rendering
                "html_users": await self.render_page(users, "chat/includes/user_status.html")

            }
        )

    async def user_update(self, event):
        await self.send_json(event)
        print('user_update', event)

    @sync_to_async
    def update_user_status(self, user, status):
        return Profile.objects.filter(user_id=user.pk).update(status=status)

    @sync_to_async
    def render_page(self, users, path):
        return render_to_string(
            path, {'users': users})
