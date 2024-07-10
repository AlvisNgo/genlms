import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.groups = ["test_room_1","test_room_2"]
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
        message = text_data_json["message"]
        username = text_data_json["username"]
        if action == 'join':
            if group_name not in self.groups:
                self.groups.append(group_name)
                await self.channel_layer.group_add(
                    group_name,
                    self.channel_name
                )
        elif action == 'leave':
            if group_name in self.groups:
                self.groups.remove(group_name)
                await self.channel_layer.group_discard(
                    group_name,
                    self.channel_name
                )
        elif action == 'send':
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