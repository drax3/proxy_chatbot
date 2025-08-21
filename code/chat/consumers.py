import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.utils import timezone

from .models import ChatRoom, Message

@database_sync_to_async
def room_exists(room_id):
    return ChatRoom.objects.filter(pk=room_id).exists()

@database_sync_to_async
def create_user_message(room_id, user, content):
    msg = Message.objects.create(
        room_id=room_id,
        sender=user if user and not isinstance(user, AnonymousUser) else None,
        role="user",
        content=content,
        timestamp=timezone.now(),
    )
    return {
        "id": msg.id,
        "room": msg.room_id,
        "sender": ({"id": msg.sender.id, "username": msg.sender.username} if msg.sender else None),
        "role": msg.role,
        "content": msg.content,
        "timestamp": msg.timestamp.isoformat(),
    }

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id= int(self.scope["url_route"]["kwargs"]["room_id"])
        self.group_name = f"room_{self.room_id}"

        if not await room_exists(self.room_id):
            await self.close(code=4404)
            return
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self,close_node):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        if not text_data:
            return
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            return

        if data.get("type") == "message.create":
            content = (data.get("content") or "").stip()
            if not content:
                return
            # create user message
            created = await create_user_message(self.room_id, self.scope.get("user"), content)
            # Broadcast to room (everyone including sender)
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "chat_message",
                    "payload": created,
                }
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event["payload"]))



