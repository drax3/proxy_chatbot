from __future__ import annotations

from celery import shared_task
from django.conf import settings
from django.db import transaction
from django.utils import timezone

from .models import ChatRoom, Message
from .gemini_client import generate_gemini_reply

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 3})
def send_message_to_gemini(self, room_id: int, user_message_id: int):
    """
    Celery task that takes the latest user message, generates a Gemini reply,
    and saves it in the same ChatRoom.
    """
    with transaction.atomic():
        room = ChatRoom.objects.select_for_update().get(pk=room_id)
        user_msg = Message.objects.select_for_update().get(
            pk=user_message_id, room=room, role="user"
        )

        # Get last 20 messages for context
        context_qs = Message.objects.filter(room=room).order_by("-timestamp")[:20]
        history = [{"role": m.role, "content": m.content} for m in reversed(list(context_qs))]

        # Call Gemini (mocked or real)
        reply_text = generate_gemini_reply(
            api_key=settings.GEMINI_API_KEY,
            model_name=settings.GEMINI_MODEL,
            history=history,
        )

        # Save AI reply
        ai_msg = Message.objects.create(
            room=room,
            sender=None,  # AI system
            role="ai",
            content=reply_text,
            timestamp=timezone.now(),
        )
        # Broadcast to websocket group
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"room_{room.id}",
            {
                "type": "chat_message",
                "payload": {
                    "id": ai_msg.id,
                    "room": room.id,
                    "sender": None,
                    "role": ai_msg.role,
                    "content": ai_msg.content,
                    "timestamp": ai_msg.timestamp.isoformat(),
                },
            }
        )
    return {
        "room_id": room_id,
        "user_message_id": user_message_id,
        "ai_message_id": ai_msg.id,
        "status": "saved",
    }
