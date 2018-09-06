from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import Room, Message
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

class RoomDetailView(LoginRequiredMixin, DetailView):
    model = Room
    template_name = 'chat/room_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = Message.objects.filter(room=self.object).select_related('author')
        return context
