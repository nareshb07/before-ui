import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from chats.models import ChatModel, UserProfileModel, ChatNotification, UserProfile
from .models import User
from django.utils import timezone
from channels.layers import get_channel_layer


class PersonalChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        my_id = self.scope['user'].id

        other_user_id = self.scope['url_route']['kwargs']['id']
        if int(my_id) > int(other_user_id):
            self.room_name = f'{my_id}-{other_user_id}'
        else:
            self.room_name = f'{other_user_id}-{my_id}'

        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        print("hello")

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        if 'file_url' in data:
            file_url = data['file_url']
            file_name = data['file_name']
           
            username = data['username']
            receiver = data['receiver']
            
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'file_url': file_url,
                    'username': username,
                    'file_name': file_name
                    
                }
            )
        else:
            message = data['message']
            username = data['username']
            receiver = data['receiver']
            
            await self.save_message(username, self.room_group_name, message, receiver)
            
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': username,
                }
            )
    
    async def chat_message(self, event):
        if 'file_url' in event:
            file_url = event['file_url']
            username = event['username']
            file_name = event['file_name']
            
            
            
            await self.send(text_data=json.dumps({
                'file_url': file_url,
                'username': username,
                'file_name': file_name,

            }))
        else:
            message = event['message']
            username = event['username']
            
            await self.send(text_data=json.dumps({
                'message': message,
                'username': username,
            }))

    async def disconnect(self, code):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    @database_sync_to_async
    def save_message(self, username, thread_name, message, receiver):
        chat_obj = ChatModel.objects.create(
            sender=username, message=message, thread_name=thread_name)
        chat_obj.save()

        my_id = self.scope['user'].id
        receiver_id = self.scope['url_route']['kwargs']['id']

        try:
            UserProfile.objects.filter(Follower_id=my_id, user_id=receiver_id).update(message_seen=True)
        except Exception as e:
            print(e)

        try:
            u = UserProfile.objects.get(user_id=my_id, Follower_id=receiver_id)
            u.last_message = timezone.now()
            u.save()
        except Exception as e:
            print(e)
