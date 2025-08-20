from django.urls import path
from .views import (
    ChatRoomListCreateView,
    MessageListCreateView,
)

urlpatterns = [
    path('chatrooms/', ChatRoomListCreateView.as_view(), name='chatroom_list_create'),
    path('chatrooms/<int:room_id>/messages/', MessageListCreateView.as_view(), name='message_list_create')
]