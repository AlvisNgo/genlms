import json;
from channels.generic.websocket import AsyncWebsocketConsumer
from django.shortcuts import get_object_or_404
from asgiref.sync import sync_to_async
from lms.models import User,Message,ChatRoom,ChatRoomUser

class ChatConsumer(AsyncWebsocketConsumer):
    
    # Generating class variables and group chats
    async def connect(self):
        self.channel_user = self.scope['url_route']['kwargs']['userid']
        self.user = await sync_to_async(User.objects.filter(id=self.channel_user).first)()
        channel_groups = await sync_to_async(list)(ChatRoom.objects.filter(chatroomuser__user_id=self.channel_user).values_list('id', flat=True))
        self.groups = [str(group) for group in channel_groups]
        self.groups.append("user_" + str(self.channel_user))
        for group in self.groups:
            await self.channel_layer.group_add(
                group,
                self.channel_name
            ) 
        await self.accept()

    # Disconnecting from all groupchats
    async def disconnect(self , close_code):
        for group in self.groups:
            await self.channel_layer.group_discard(
                group,
                self.channel_name
            )

    # Recieving messages from client side
    async def receive(self, text_data):
        #Putting common json messages into variables
        text_data_json = json.loads(text_data)
        print(text_data_json)
        action = text_data_json["action"]
        group_id = str(text_data_json["group"])
        try:
            chatroom = await sync_to_async(ChatRoom.objects.filter(id=group_id).first)()
        except:
            print("Unable to get chatroom")
        username = text_data_json["username"]
        user = await sync_to_async(User.objects.filter(first_name=username).first)()

        # if user is joining a chatroom, add chatroom to list of groups
        if action == 'join':
            if (group_id != group for group in self.groups):
                self.groups.append(group_id)
                await self.channel_layer.group_add(
                    group_id,
                    self.channel_name
                )
        # if user is leaving a chatroom
        elif action == 'leave':
            for group in self.groups :
                if (group_id == group and self.channel_user == str(user.id)):
                    self.groups.remove(group)
                    #remove user from database
                    roomUser =  await sync_to_async(ChatRoomUser.objects.filter(chatroom_id=chatroom,user_id=user.id).first)()
                    await self.channel_layer.group_discard(
                        group,
                        self.channel_name
                    )
                    await sync_to_async(roomUser.delete)()
                    
        # if user is creating a chatroom 
        elif action == 'create':
            groupname = text_data_json["groupname"]
            #create new chatroom in database
            new_chatroom = ChatRoom(name= groupname,creator_id=user.id)
            await sync_to_async(new_chatroom.save)()
            #retrieve database record with chatroom id
            new_chatroom =  await sync_to_async(ChatRoom.objects.filter(name = groupname,creator_id=user.id).order_by('-created_at').first)()
            members = text_data_json["members"]
            for member in members:
                if (member != self.user.first_name ):
                    try:
                        #create chatroom user in database
                        member_check = await sync_to_async(User.objects.filter(username=str(member)).first)()
                        new_chatroom_user = ChatRoomUser(chatroom= new_chatroom ,user=member_check)
                        await sync_to_async(new_chatroom_user.save)()
                        new_user_group = "user_" +str(member_check.id)

                        #connect to user websocket group
                        await self.channel_layer.group_add(
                            new_user_group,
                            self.channel_name
                        )
                        #send client side to update html
                        await self.channel_layer.group_send(
                            new_user_group,
                        {
                            "type": "send_message",
                            "action": "new_chat",
                            "group" : new_chatroom.id,
                                "message": {
                                    "creator":user.id,
                                    "member": str(new_chatroom_user.user_id),
                                    "group_name":new_chatroom.name,
                                },
                            "sender_channel": self.channel_name
                        }
                        )
                        # remove group from grouplist
                        await self.channel_layer.group_discard(
                            new_user_group,
                            self.channel_name
                        )
                    except Exception as e:
                        print(e)

        # if editing an existing chatroom
        elif action == 'edit_group':
            # finding current members from database
            current_members = await sync_to_async(list)(ChatRoomUser.objects.filter(chatroom_id = chatroom.id).select_related('user').values_list('user__username', flat=True))
            # getting memberlist from client side
            members = text_data_json["members"]
            # comparing both lists
            remove_members =(list(set(current_members) - set(members)))
            add_members = (list(set(members) - set(current_members)))
            # removing members
            for member in remove_members:
                    try:
                        member_check = await sync_to_async(User.objects.filter(username=member).first)()
                        user_group = "user_" +str(member_check.id)
                        await self.channel_layer.group_add(
                            user_group,
                            self.channel_name
                        )
                        await self.channel_layer.group_send(
                            user_group,
                        {
                            "type": "send_message",
                            "action": "leave",
                            "group" : chatroom.id,
                                "message": {
                                    "creator":user.id,
                                    "member": str(member_check.id),
                                    "group_name":chatroom.name,
                                },
                            "sender_channel": self.channel_name
                        }
                        )
                        await self.channel_layer.group_discard(
                            user_group,
                            self.channel_name
                        )
                        roomUser =  await sync_to_async(ChatRoomUser.objects.filter(chatroom_id=chatroom,user_id=member_check.id).first)()
                        await sync_to_async(roomUser.delete)()    
                    except Exception as e:
                        print(e)
            # adding members         
            for member in add_members:
                try:
                    member_check = await sync_to_async(User.objects.filter(username=member).first)()
                    new_chatroom_user = ChatRoomUser(chatroom_id = chatroom.id,user=member_check)
                    await sync_to_async(new_chatroom_user.save)()
                    new_user_group = "user_" +str(member_check.id)
                    await self.channel_layer.group_add(
                        new_user_group,
                        self.channel_name
                    ) 
                    await self.channel_layer.group_send(
                        new_user_group,
                    {
                        "type": "send_message",
                        "action": "new_chat",
                        "group" : chatroom.id,
                            "message": {
                                "creator":user.id,
                                "member": str(new_chatroom_user.user_id),
                                "group_name":chatroom.name,
                            },
                        "sender_channel": self.channel_name
                    }
                    )
                    await self.channel_layer.group_discard(
                        new_user_group,
                        self.channel_name
                    )
                except Exception as e:
                    print(e)
        # if chatroom is destroyed
        elif action == 'destroy':
            for group in self.groups :
                # broadcast for users to leave group
                if (group_id == group):
                    room =  await sync_to_async(ChatRoom.objects.filter(creator=user,id=group_id).first)()
                    self.groups.remove(group)
                    await self.channel_layer.group_send(
                        group_id,
                        {
                            "type": "send_message",
                            "action": "leave",
                            "group" : group_id,
                                "message": {
                                "member": "all" 
                                }
                        }
                    )
                    await self.channel_layer.group_discard(
                        group,
                        self.channel_name
                    )
                    await sync_to_async(room.delete)()
        # retrieve users chatrooms
        elif action == 'retrieve_chat_details':
            chat_room_users = await sync_to_async(list)(ChatRoomUser.objects.filter(chatroom_id=group_id))
            data = []
            data.append({
                'userid': chatroom.creator_id,
                'uid': await sync_to_async(lambda: chatroom.creator.username)(),
                'username': await sync_to_async(lambda: chatroom.creator.first_name)(),
                'message': "creator"
            })
            for user in chat_room_users:
                if user.user_id != chatroom.creator_id:
                    user_uid = await sync_to_async(lambda: user.user.username)()
                    user_firstname = await sync_to_async(lambda: user.user.first_name)()
                    data.append({
                        'userid': user.user_id,
                        'uid': user_uid,
                        'username': user_firstname,
                        'message': "member"
                    })
            await self.send(json.dumps({
                    "type": "send_message",
                    "action": "chat_details",
                    "group" : group_id,
                    "message": data
                })
            )
        # sending a message
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
        # editing an existing message 
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
        #delete a message
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
        # retrieve chatroom messages
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
    # function for sending message out
    async def send_message(self , event) : 
        action = event["action"]
        message = event["message"]
        group = event["group"]
        await self.send(text_data = json.dumps({"action":action, "message":message , "group":group}))