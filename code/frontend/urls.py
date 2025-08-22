from django.urls import path
from .views import LoginView, RoomsView, ChatView

urlpatterns = [
    path("", LoginView.as_view(), name="login"),
    path("rooms/", RoomsView.as_view(), name="rooms"),
    path("chat/<int:room_id>/", ChatView.as_view(), name="chat"),
]
