from django.urls import path

from . import views

app_name = 'chat'
urlpatterns = [
    path('rooms/', views.ChatRoomsView.as_view(), name='chatrooms'),
    path('rooms/create/', views.RoomCreateView.as_view(), name='room_create'),
]