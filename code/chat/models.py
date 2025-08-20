from email.policy import default
from enum import unique
from secrets import choice

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatRoom(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_rooms")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Message(models.Model):
    ROLE_CHOICES =  (
        ("user", "User"),
        ("ai", "AI"),
        ("system", "System"),
    )

    room = models.ForeignKey(ChatRoom, related_name="messages", on_delete=models.CASCADE)
    sender = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="messages")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="user")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        who = self.sender.email if self.sender else self.role
        return f"[{self.timestamp}] {who}: {self.content[:30]}"