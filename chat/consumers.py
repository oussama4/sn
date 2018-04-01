from channels.generic.websocket import AsyncJsonWebsocketConsumer

from .sync_to_async import get_room_or_error, get_user_or_error, save_message

class ChatConsumer(AsyncJsonWebsocketConsumer):
    """
    handles websocket connections and messages
    """

    async def connect(self):
        room_id = self.scope['url_route']['kwargs']['pk']
        room_name = await get_room_or_error(room_id)
        await self.channel_layer.group_add(room_name, self.channel_name)
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
            'room': room_id,
            'user': user_id,
            'message': msg
            })
        await save_message(room, user, msg)

    async def chat_message(self, event):
        """
        called when a message is to room group
        """

        self.send_json({
            'room': event['room'],
            'user': event['user'],
            'message': event['message']
        })