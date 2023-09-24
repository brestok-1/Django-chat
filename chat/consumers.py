import json

from channels.generic.websocket import AsyncWebsocketConsumer


class NewMessageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "new-message"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def new_message(self, event):
        username = event['message']['username']
        text = event['message']['text']
        time_created = event['message']['time_created']
        await self.send(text_data=json.dumps({
            'username': username,
            'text': text,
            'time_created': time_created
        }))
