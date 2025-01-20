# chat/models.py
from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender} to {self.receiver}: {self.content[:20]}"

# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from .models import Message  # Correct import: from .models import Message
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']  # Get the user object
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.room_group_name = f'chat_{self.user_id}'

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
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        receiver_id = text_data_json['receiver_id']

        # Use the user object directly
        await self.save_message(self.user.id, receiver_id, message)

        await self.channel_layer.group_send(
            f'chat_{receiver_id}',
            {
                'type': 'chat_message',
                'message': message,
                'sender_id': self.user.id,
            }
        )
        await self.channel_layer.group_send(
            f'chat_{self.user.id}',
            {
                'type': 'chat_message',
                'message': message,
                'sender_id': self.user.id,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender_id = event['sender_id']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender_id': sender_id
        }))

    @database_sync_to_async
    def save_message(self, sender_id, receiver_id, message):
        sender = User.objects.get(id=sender_id)
        receiver = User.objects.get(id=receiver_id)
        Message.objects.create(sender=sender, receiver=receiver, content=message)

# chat/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<user_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
]

# mysite/asgi.py (No changes usually needed here if you followed the Django Channels setup)
import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import chat.routing  # Import your app's routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns  # Use your app's routing here
        )
    ),
})

# chat/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message

@login_required
def chat_view(request, user_id):
    messages = Message.objects.filter(sender=request.user, receiver_id=user_id) | Message.objects.filter(sender_id=user_id, receiver=request.user)
    messages = messages.order_by('timestamp')
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat/chat.html', {'messages': messages, 'users': users, 'receiver_id': user_id})

# chat/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('chat/<int:user_id>/', views.chat_view, name='chat'),
]