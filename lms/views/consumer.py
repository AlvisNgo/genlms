import json;
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from lms.models import User,Message,ChatRoom,ChatRoomUser

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        channel_user = self.scope['url_route']['kwargs']['userid']
        channel_groups = await sync_to_async(list)(ChatRoom.objects.filter(chatroomuser__user_id=channel_user).values_list('id', flat=True))
        self.groups = [str(group) for group in channel_groups]
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
        group_id = text_data_json["group"]
        chatroom = await sync_to_async(ChatRoom.objects.filter(id=group_id).first)()
        username = text_data_json["username"]
        user = await sync_to_async(User.objects.filter(first_name=username).first)()
        if action == 'join':
            # not done
            if (group_id != group for group in self.groups):
                self.groups.append(chatroom)
                await self.channel_layer.group_add(
                    group_id,
                    self.channel_name
                )
        elif action == 'leave':
            for group in self.groups :
                if (group_id == group):
                    self.groups.remove(group)
                    roomUser =  await sync_to_async(ChatRoomUser.objects.filter(chatroom_id=chatroom,user_id=user).first)()
                    await self.channel_layer.group_discard(
                        group,
                        self.channel_name
                    )
                    await sync_to_async(roomUser.delete)()
        elif action == 'destroy':
            for group in self.groups :
                if (group_id == group):
                    room =  await sync_to_async(ChatRoom.objects.filter(creator=user).first)()
                    self.groups.remove(group)
                    await self.channel_layer.group_send(
                        group_id,
                        {
                            "type": "send_message",
                            "action": "leave",
                            "group" : group_id,
                                "message": {
                                }
                        }
                    )
                    await self.channel_layer.group_discard(
                        group,
                        self.channel_name
                    )
                    await sync_to_async(room.delete)()

        elif action == 'send':
            message = text_data_json["message"]
            new_message = Message(user=user,chatroom=chatroom,content= message)
            await sync_to_async(new_message.save)()
            database_message = await sync_to_async(Message.objects.filter(chatroom_id = chatroom, user=user ,content=message).first)()
            if (group_id == group for group in self.groups):
                await self.channel_layer.group_send(
                    group_id,
                    {
                        "type": "send_message",
                        "action": "message",
                        "group" : group_id,
                            "message": {
                                "username":username,
                                "id": database_message.id,
                                "message": database_message.content
                            }
                    }
                )
        elif action == 'edit':
            message = text_data_json["message"]
            messageid = text_data_json["messageid"]
            database_message = await sync_to_async(Message.objects.filter(id=messageid).first)()
            database_message.content = message
            await sync_to_async(database_message.save)()
            if (group_id == group for group in self.groups):
                await self.channel_layer.group_send(
                    group_id,
                    {
                        "type": "send_message",
                        "action": "edit",
                        "group" : group_id,
                            "message": {
                                "username":username,
                                "id": messageid,
                                "message": message
                            }
                    }
                )
        elif action == 'retrieve_chat_details':
            chat_room = await sync_to_async(list)(ChatRoom.objects.filter(chatroom_id=group_id).first)()
            chat_room_users = await sync_to_async(list)(ChatRoomUser.objects.filter(chatroom_id=group_id))
            data = []
            for user in chat_room_users:
                user_firstname = await sync_to_async(lambda: chat_room_users.first_name)()
                content = message.content
                message_id = message.id
                data.append({
                    'username': user_firstname,
                    'message': content
                })
            await self.send(json.dumps({
                    "type": "send_message",
                    "action": "chat_details",
                    "group" : group_id,
                    "message": data
                })
            )

        elif action == 'retrieve_chat_history':
            history = await sync_to_async(list)(Message.objects.filter(chatroom_id=group_id).order_by('timestamp'))
            data = []

            for message in history:
                user_firstname = await sync_to_async(lambda: message.user.first_name)()
                content = message.content
                message_id = message.id
                data.append({
                    'username': user_firstname,
                    'id': message_id,
                    'message': content
                })
            await self.send(json.dumps({
                    "type": "send_message",
                    "action": "chat_history",
                    "group" : group_id,
                    "message": data
                })
            )
        elif action == 'delete':
            messageid = text_data_json["messageid"]
            message_retrieved = await sync_to_async((Message.objects.filter(id=messageid).first))()
            await self.channel_layer.group_send(
                group_id,
                {
                    "type": "send_message",
                    "action": "delete",
                    "group" : group_id,
                        "message": {
                            "id": message_retrieved.id
                        }
                }
            )
            await sync_to_async(message_retrieved.delete)()

    async def send_message(self , event) : 
        action = event["action"]
        message = event["message"]
        group = event["group"]
        await self.send(text_data = json.dumps({"action":action, "message":message , "group":group}))