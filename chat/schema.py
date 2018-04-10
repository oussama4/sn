import graphene
from graphene_django.types import DjangoObjectType

from .models import Room, Message

class RoomType(DjangoObjectType):
    class Meta:
        model = Room

class MessageType(DjangoObjectType):
    class Meta:
        model = Message

class Query(object):
    rooms = graphene.List(RoomType)
    messages = graphene.List(MessageType,
                             room=graphene.NonNull(graphene.Int),
                             limit=graphene.NonNull(graphene.Int),
                             offset=graphene.NonNull(graphene.Int))

    def resolve_rooms(self, info, **kwargs):
        return Room.objects.all()

    def resolve_messages(self, info, **kwargs):
        #user_id = kwargs.get('user')
        room_id = kwargs.get('room')
        limit = kwargs.get('limit')
        offset = kwargs.get('offset')

        return Message.objects.filter(
                room_id=room_id
                ).select_related('author', 'room')[offset:limit]