from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db import transaction

from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer
from users.serializers import ProfileSerializer

from .tasks import send_message_to_gemini

User = get_user_model()

class ChatRoomListCreateView(generics.ListCreateAPIView):
    queryset = ChatRoom.objects.all().order_by("-created_at")
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class MessageListCreateView(generics.ListCreateAPIView):

    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        room_id =  self.kwargs["room_id"]
        return Message.objects.filter(room_id=room_id).order_by("timestamp")

    def create(self, request, *args, **kwargs):
        room_id = kwargs["room_id"]

        try:
            room = ChatRoom.objects.get(pk=room_id)
        except ChatRoom.DoesNotExist:
            return Response({"detail": "chatroom not found"}, status=404)

        content = request.data.get("content", "").strip()
        if not content:
            return Response({"detail": "content is required"}, status=400)

        with transaction.atomic():
            user_message = Message.objects.create(
                room=room,
                sender=request.user,
                role="user",
                content=content,
            )
        async_result = send_message_to_gemini.delay(room_id=room.id, user_message_id=user_message.id)

        payload = {
            "message": MessageSerializer(user_message).data,
            "task_id": async_result.id,
            "status": "queued",
        }
        return Response(payload, status=status.HTTP_202_ACCEPTED)