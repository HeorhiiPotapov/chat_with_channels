import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import ChatRoom, Message
from .utilities import encode_img_binary, decode_img_binary
from django.core.files.temp import NamedTemporaryFile

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):

    async def upload_response(self, data):
        print(data)
        # self.attrs = {
        #     'file_obj': NamedTemporaryFile(delete=False),
        #     'total_size': int(data['size'])
        # }
        # await self.send(text_data=json.dumps({
        #     'option': 'dispatch',
        #     'action': 'ready'
        # }))

    # async def upload_chunk(self, data):
    #     total_size = self.attrs.get('total_size')
    #     file_obj = self.attrs.get('file_obj')
    #     print(type(data))
    #     if not total_size or not file_obj:
    #         pass
    #         # return self.error('Invalid request. Please try again.')

    #     self.attrs['file_obj'].write(data)
    #     size = self.attrs['file_obj'].tell()
    #     print(size)
    #     await self.send(text_data=json.dumps({
    #         'option': 'dispatch',
    #         'action': 'progress',
    #         'file_size': str(size)
    #     }))
    #     if size >= total_size:
    #         # await self.upload_complete(self.attrs['file_obj'])
    #         self.attrs['file_obj'].flush()
    #         await self.send(text_data=json.dumps({
    #             'option': 'dispatch',
    #             'action': 'complete'
    #         }))


# ============ base methods ==============


    @ database_sync_to_async
    def get_user(self):
        return User.objects.get(name=self.scope['user'].name)

    @ database_sync_to_async
    def get_room(self):
        return ChatRoom.objects.get(name=self.room_name)

# ============ add or remove members ===========

    @ database_sync_to_async
    def add_or_remove_member(self, action):
        if action == 'add':
            self.room.members.add(self.user)
        elif action == 'remove':
            self.room.members.remove(self.user)

# =============== message with image upload ==============

    async def image_message_task(self, data):
        print(data['value'])
        image = decode_img_binary(data['value'], data['format'])
        message = await self.save_image_message(image)
        msg_data = {
            'option': 'image',
            'value': message
        }
        await self.send_chat_message(msg_data)

    @ database_sync_to_async
    def save_image_message(self, image):
        message = Message.objects.create(
            room=self.room,
            sender=self.user,
            text='new file upload',
            image=image
        )
        message.save()
        return self.message_to_json(message)

# ================ SERIALIZE MESSAGES ======================

    def messages_to_json(self, messages):
        result = []
        for i in messages:
            result.append(self.message_to_json(i))
        return result

    def message_to_json(self, message):
        context = {
            'id': message.id,
            'sender': message.sender.name,
            'room': message.room.name,
            'text': message.text,
            'timestamp': str(message.timestamp.strftime('%I:%M')),
        }
        if message.image:
            context['image'] = encode_img_binary(message.image.path)
        return context

# ================= LOAD MESSAGE HYSTORY =====================

    async def fetch_task(self, data):
        messages = await self.fetch()
        await self.send_fetch(messages)

    @ database_sync_to_async
    def fetch(self):
        messages = Message.objects.filter(room=self.room)
        return {
            'option': 'fetch',
            'messages': self.messages_to_json(messages)
        }

# ================= NEW MESSAGE CREATE =====================

    async def new_message_task(self, data):
        await self.send_chat_message(
            await self.new_message(data)
        )

    @ database_sync_to_async
    def new_message(self, data):
        message = Message.objects.create(
            sender=self.user,
            room=self.room,
            text=data['message'])
        message.save()
        return {
            'option': data['option'],
            'message': self.message_to_json(message)
        }

# ==================== CONNECT =========================

    async def connect(self):
        print('CONNECT -->> ')
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group = 'chat_%s' % self.room_name
        self.user = await self.get_user()
        self.room = await self.get_room()
        await self.add_or_remove_member(action='add')
        await self.channel_layer.group_add(
            self.room_group,
            self.channel_name
        )
        await self.accept()

# =================== DISCONNECT =====================

    async def disconnect(self, close_code):
        print('DISCONNECT -->>')

        # commented just for now
        # await self.add_or_remove_member(action='remove')

        await self.channel_layer.group_discard(
            self.room_group,
            self.channel_name
        )

# ================ RECEIVE FROM WEBSOCKET ===================

    options = {
        'fetch': fetch_task,
        'new_message': new_message_task,
        'image': image_message_task,
        'upload_request': upload_response
    }

    async def receive(self, text_data=None, bytes_data=None):
        print('RECEIVE -->>')
        if bytes_data:
            data = bytes_data
            await self.upload_chunk(data)
        else:
            data = json.loads(text_data)
            await self.options[data['option']](self, data)

# ================= SEND MESSAGE =====================

    async def send_chat_message(self, message):
        print('CHAT_MESSAGE -->>')
        await self.channel_layer.group_send(
            self.room_group,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))

    async def send_fetch(self, message):
        await self.send(text_data=json.dumps(message))
