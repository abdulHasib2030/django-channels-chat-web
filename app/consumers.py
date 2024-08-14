from channels.generic.websocket import  AsyncJsonWebsocketConsumer
from app.models import *
from django.contrib.auth.models import User
from datetime import datetime
import json
from channels.db import database_sync_to_async

class MyAsyncJsonWebSocketConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        print("Websocket Connect:")
    
        user_id = self.scope['user'].id   # login user
        group_id = self.scope['url_route']['kwargs']['id'] # chating user
        
        user1 = await database_sync_to_async(User.objects.get)(pk=user_id)
        user2 = await database_sync_to_async(User.objects.get)(pk=int(group_id))
        
        self.group_name = f"{min(user1.username, user2.username)}_{max(user1.username, user2.username)}" # create group name for two user
        await self.channel_layer.group_add(self.group_name, self.channel_name) # add group for channel layer
        
        # Accepting the WebSocket connection
        await self.accept()

    async def receive_json(self, content, **kwargs):
        user =self.scope['user'] #login user
        receive = (content['id']) # chantting user id
    
        message = content['msg']
        date = datetime.now()
        print(date)
        obj_date1 = date.strftime("%Y-%m-%d %I:%M:%S %p")
        obj_date =datetime.strptime(obj_date1, "%Y-%m-%d %I:%M:%S %p")
        print(type(obj_date))
        user2 = await database_sync_to_async(User.objects.get)(pk = int(receive))
        message = DirectMessage(sender = user, receiver = user2, content = message, timestamp=obj_date)
        await database_sync_to_async(message.save)()
        content['username'] = user2.username # frontend send username for chatting user
        content['date'] = obj_date1 # frontend send date
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type':'chat.message',
                'msg':content,

            }
        )


    
    async def chat_message(self, event):
        print(event)
        await self.send_json({
            'msg':event['msg'],
            
        })

    async def disconnect(self, code):
        # print('websockent disconnect', code)
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_layer
        )



#  User Online / Offline Status class 
class onlineStatusAsyncJonWebsocketConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'user'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
    
    async def receive_json(self, content, **kwargs):
        username = content['username']
        connection_type = content['type']
        print(username, connection_type)

        user =await database_sync_to_async(User.objects.get)(username= json.loads(username))
        onlineStatus =await database_sync_to_async(OnlineStatusModel.objects.get)(user = user)

        if connection_type == 'open':
            onlineStatus.status = True
            await database_sync_to_async(onlineStatus.save)()
        else:
            onlineStatus.status = False
            await database_sync_to_async(onlineStatus.save)()
        print(onlineStatus.status, "Hello Abdul Hasib", onlineStatus.name)


        data = {
            'username':username,
            'online':onlineStatus.status
        }
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'chat.message',
                'msg':data,
            }
        )
    
    async def chat_message(self, event):
        await self.send_json(
        {
            'msg':event['msg']
        }
        )

    async def disconnect(self, code):
        user = self.scope['user'].id
        online = await database_sync_to_async(OnlineStatusModel.objects.get)(pk = user)
        online.status = False
        await database_sync_to_async(online.save)()
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_layer,
        )