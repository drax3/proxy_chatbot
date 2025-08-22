from django.views.generic import TemplateView

class LoginView(TemplateView):
    template_name = "frontend/login.html"

class RoomsView(TemplateView):
    template_name = "frontend/rooms.html"

class ChatView(TemplateView):
    template_name = "frontend/chat.html"
