import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from lms.models import User,Message,ChatRoom,ChatRoomUser;

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        channel_user = self.scope['url_route']['kwargs']['userid']
        self.groups = await sync_to_async(list)(ChatRoom.objects.filter(chatroomuser__user_id=channel_user))
        for group in self.groups:
            await self.channel_layer.group_add(
                str(group.id),
                self.channel_name
            ) 
        await self.accept()

    async def disconnect(self , close_code):
        for group in self.groups:
            await self.channel_layer.group_discard(
                str(group.id),
                self.channel_name
            )
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json["action"]
        group_id = text_data_json["group"]
        chatroom = await sync_to_async(ChatRoom.objects.filter(id=group_id).first)()
        username = text_data_json["username"]
        user = await sync_to_async(User.objects.filter(first_name=username).first)()
        if action == 'join':
            if (group_id != group.id for group in self.groups):
                self.groups.append(group_id)
                await self.channel_layer.group_add(
                    group_id,
                    self.channel_name
                )
        elif action == 'leave':
            if (group_id == group.id for group in self.groups):
                # not tested
                roomUser =  await sync_to_async(ChatRoomUser.objects.filter(id=id).first)()
                await sync_to_async(roomUser.delete())
                self.groups.remove(group_id)
                await self.channel_layer.group_discard(
                    group_id,
                    self.channel_name
                )
        elif action == 'send':
            message = text_data_json["message"]
            new_message = Message(user=user,chatroom=chatroom,content= message)
            await sync_to_async(new_message.save)()
            if (group_id == group.id for group in self.groups):
                await self.channel_layer.group_send(
                    group_id,
                    {
                        "type": "send_message",
                        "content": "message",
                        "group" : group_id,
                        "username" : username ,
                        "message": message,
                    }
                )
        elif action == 'retrieve':
            history = await sync_to_async(list)(Message.objects.filter(chatroom_id=group_id).order_by('timestamp'))
            data = []

            for message in history:
                user_firstname = await sync_to_async(lambda: message.user.first_name)()
                content = message.content
                data.append({
                    'username': user_firstname,
                    'message': content,
                })

            if (group_id == group.id for group in self.groups):
                await self.channel_layer.group_send(
                    group_id,
                    {
                        "type": "send_message",
                        "content": "chat_history",
                        "group" : group_id,
                        "username" : username ,
                        "message": data
                    }
                )
    async def send_message(self , event) : 
        content = event["content"]
        message = event["message"]
        username = event["username"]
        group = event["group"]
        await self.send(text_data = json.dumps({"action":content, "message":message ,"username":username, "group":group}))