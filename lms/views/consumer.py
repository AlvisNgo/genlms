import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from lms.models import User,Message,ChatRoom,ChatRoomUser;

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        channel_user = self.scope['url_route']['kwargs']['userid']
        self.groups = await sync_to_async(list)(ChatRoom.objects.filter(chatroomuser__user_id=channel_user).values_list('name', flat=True))
        for group in self.groups:
            await self.channel_layer.group_add(
                group,
                self.channel_name
            ) 
        await self.accept()

    async def disconnect(self , close_code):
        for group in self.groups:
            await self.channel_layer.group_discard(
                group,
                self.channel_name
            )
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json["action"]
        group_name = text_data_json["group"]
        chatroom = await sync_to_async(ChatRoom.objects.filter(name=group_name).first)()
        message = text_data_json["message"]
        username = text_data_json["username"]
        user = await sync_to_async(User.objects.filter(first_name=username).first)()
        if action == 'join':
            if group_name not in self.groups:
                self.groups.append(group_name)
                await self.channel_layer.group_add(
                    group_name,
                    self.channel_name
                )
        elif action == 'leave':
            if group_name in self.groups:
                # not tested
                roomUser =  await sync_to_async(ChatRoomUser.objects.filter(id=id).first)()
                await sync_to_async(roomUser.delete())
                self.groups.remove(group_name)
                await self.channel_layer.group_discard(
                    group_name,
                    self.channel_name
                )
        elif action == 'send':
            new_message = Message(user=user,chatroom=chatroom,content= message)
            await sync_to_async(new_message.save)()
            if group_name in self.groups:
                await self.channel_layer.group_send(
                    group_name,
                    {
                        "type": "send_message",
                        "group" : group_name,
                        "message": message,
                        "username" : username ,
                    }
                )

    async def send_message(self , event) : 
        message = event["message"]
        username = event["username"]
        group = event["group"]
        await self.send(text_data = json.dumps({"message":message ,"username":username, "group":group}))