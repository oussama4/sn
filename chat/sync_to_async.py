from channels.db import database_sync_to_async

from accounts.models import User
from .models import Room, Message

@database_sync_to_async
def get_room_or_error (room_id):
    room = Room.objects.get(pk=room_id)
    return room

@database_sync_to_async
def get_user_or_error(user_id):
    user = User.objects.get(pk=user_id)
    return user

@database_sync_to_async
def save_message(room, author, body):
    Message.objects.create(author=author, room=room, body=body)