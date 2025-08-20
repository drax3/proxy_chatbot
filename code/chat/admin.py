from django.contrib import admin
from .models import ChatRoom, Message


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_by", "created_at")
    search_fields = ("name", "created_by__username")
    list_filter = ("created_at",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "room", "role", "sender", "short_content", "timestamp")
    list_filter = ("role", "timestamp", "room")
    search_fields = ("content", "sender__username")

    def short_content(self, obj):
        return (obj.content[:60] + "…") if len(obj.content) > 60 else obj.content
