import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import ChatMessages
from accounts.models import BaseUser
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.sender_id = self.scope['url_route']['kwargs']['sender_id']
        self.receiver_id = self.scope['url_route']['kwargs']['receiver_id']
        self.room_channel_name = f'chat_{min(self.sender_id, self.receiver_id)}_{max(self.sender_id, self.receiver_id)}'

        # Connect to the individual channel for this pair
        await self.channel_layer.group_add(
            self.room_channel_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_channel_name,
            self.channel_name
        )

    @database_sync_to_async
    def create_message(self, message, sender, receiver):
        message_obj = ChatMessages.objects.create(
            message=message,
            sender=sender,
            receiver=receiver
        )
        return message_obj
    
    @database_sync_to_async
    def get_user(self, id):
        return BaseUser.objects.get(id=id)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender_id = self.scope['url_route']['kwargs']['sender_id']
        receiver_id = self.scope['url_route']['kwargs']['receiver_id']
        receiver = await self.get_user(receiver_id)
        sender = await self.get_user(sender_id)
        print('===================',receiver,'=================',sender)

        # Create a new message object and save it to the database
        message_obj = await self.create_message(message, sender, receiver)
        first_name = sender.first_name
        

        # Send the message to the individual channel for this pair
        await self.channel_layer.group_send(
            self.room_channel_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender_id,
                'timestamp': str(message_obj.timestamp)
            }
        )

    async def chat_message(self, event):
        message = event['message']
        timestamp = event['timestamp']
        sender = event['sender']

        # Send the message to the websocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'timestamp': timestamp
        }))