# ride_app/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .services import LiveLocationService

class DriverLocationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.ride_id = self.scope['url_route']['kwargs']['ride_id']
        self.room_group_name = f'ride_{self.ride_id}'
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json['type']
        
        if message_type == 'location_update':
            # Driver sending location update
            driver_id = text_data_json['driver_id']
            latitude = text_data_json['latitude']
            longitude = text_data_json['longitude']
            
            # Store in MongoDB
            LiveLocationService.store_live_location(driver_id, latitude, longitude)
            
            # Send to all customers in this ride group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'location_update',
                    'driver_id': driver_id,
                    'latitude': latitude,
                    'longitude': longitude,
                    'timestamp': text_data_json.get('timestamp')
                }
            )
    
    # Receive message from room group
    async def location_update(self, event):
        # Send location update to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'location_update',
            'driver_id': event['driver_id'],
            'latitude': event['latitude'],
            'longitude': event['longitude'],
            'timestamp': event['timestamp']
        }))

class RideConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.room_group_name = f'user_{self.user_id}'
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    # Receive ride status updates
    async def ride_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'ride_update',
            'ride_id': event['ride_id'],
            'status': event['status'],
            'driver_id': event.get('driver_id'),
            'message': event.get('message')
        }))