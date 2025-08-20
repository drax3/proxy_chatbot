from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ChatRoom, Message
from users.serializers import ProfileSerializer


class ChatRoomSerializer(serializers.ModelSerializer):
    created_by = ProfileSerializer(read_only=True)

    class Meta:
        model = ChatRoom
        fields = ["id", "name", "created_by", "created_at"]

class MessageSerializer(serializers.ModelSerializer):
    sender = ProfileSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ["id", "room", "sender", "role", "content", "timestamp"]
        read_only_fields = ["role", "timestamp", "sender"]

