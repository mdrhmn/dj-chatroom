
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from .models import *
import json
from django.core.serializers import serialize


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
		Message.objects.create(username=username, room=Room.objects.get(
			name=room), content=message)

	@sync_to_async
	def get_message_date_added(self, username, message):
		# Serializer waits for normal queryset, not ValuesQuerySet (which is returned by values).
		# If you want to query only certain fileds, use only.
		date_added = Message.objects.filter(content=message,
											username=username)
		
		# return JsonResponse({'date_added': list(date_added)})
		return json.loads(serialize('json', date_added))[0]['fields']['date_added']
		