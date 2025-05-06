import json
from channels.generic.websocket import AsyncWebsocketConsumer

class DataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print("WebSocket Connected")

    async def disconnect(self, close_code):
        print("WebSocket Disconnected")

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            print("Received from ESP:", data)
        except json.JSONDecodeError:
            print("Invalid JSON received")
