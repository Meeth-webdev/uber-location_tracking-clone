from .redis_manager import redis_manager
from channels.generic.websocket import AsyncWebsocketConsumer
import json 


class OptimizedDriverLocationConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.ride_id=self.scope['url_route']['kwargs']['ride_id']

        await self.accept()

        redis_manager.subscribe_to_ride(self.ride_id,self)

    async def disconnect(self, code):
        redis_manager.unsubscribe_to_ride(self.ride_id,self)

    async def receive(self, text_data = None):
        
        data=json.loads(text_data)

        if data['type']=='location_update':
            redis_manager.publish_location(self.ride_id,data)

    async def send_redis_message(self,message):
        """Called by redis manager when new message arrives"""        

        from asgiref.sync import async_to_sync
        async_to_sync(self.send)(text_data=message)