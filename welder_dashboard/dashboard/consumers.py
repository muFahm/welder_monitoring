import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import SensorRecord
from datetime import datetime
from asgiref.sync import sync_to_async

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
            
            # Parsing timestatmp yang salah format
            try:
                timestamp = datetime.fromisoformat(data["timestamp"])
            except Exception:
                timestamp = datetime.now()

            # Save data to database async
            await self.save_sensor_data (data, timestamp)
        except json.JSONDecodeError:
            print("Invalid JSON received")

    @sync_to_async
    def save_sensor_data(self, data, timestamp):
        SensorRecord.objects.create(
            gx = data.get ("gx", 0),
            gy = data.get ("gy", 0),
            gz = data.get ("gz", 0),
            ax = data.get ("ax", 0.0),
            ay = data.get ("ay", 0.0),
            az = data.get ("az", 0.0),
            mx = data.get ("mx", 0.0),
            my = data.get ("my", 0.0),
            mz = data.get ("mz", 0.0),
            timestamp = timestamp,
        )