from django.utils.timezone import now
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from .sync_to_async import get_room_or_error, get_user_or_error, save_message

class ChatConsumer(AsyncJsonWebsocketConsumer):
    """
    handles websocket connections and messages
    """

    async def connect(self):
        room_id = self.scope['url_route']['kwargs']['pk']
        print ('room id : ' + str(room_id))
        room = await get_room_or_error(room_id)
        await self.channel_layer.group_add(room.name, self.channel_name)
        print('connection established')
        await self.accept()

    async def disconnect(self, code):
        pass

    async def receive_json(self, content):
        """
        called when a message is received from the websocket
        """

        room_id = content.get('room')
        user_id = content.get('user')
        msg = content.get('message')
        room = await get_room_or_error(room_id)
        user = await get_user_or_error(user_id)
        await self.channel_layer.group_send(
            room.name, 
            {
            'type': 'chat_message',
            'room': room_id,
            'user': user_id,
            'message': msg
            })
        await save_message(room, user, msg)

    async def chat_message(self, event):
        """
        called when a message is to room group
        """

        print('message: ' + event['message'])
        await self.send_json({
            'room': event['room'],
            'user': event['user'],
            'message': event['message'],
            'created': str(now())
        })