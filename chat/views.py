from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import Room
from .forms import RoomForm

class ChatRoomsView(LoginRequiredMixin, ListView):
    model = Room
    context_object_name = 'rooms'
    template_name = 'chat/rooms.html'

class RoomCreateView(LoginRequiredMixin, CreateView):
    form_class = RoomForm
    success_url = reverse_lazy('chat:chatrooms')
    template_name = 'chat/create.html'

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)
