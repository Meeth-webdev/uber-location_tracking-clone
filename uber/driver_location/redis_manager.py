import redis
import json 
import threading

class Redis_Manager:
    def __init__(self):
        self.redis_client=redis.Redis(host='localhost',port=6379,db=0,decode_responses=True)
        self.subscribers={}

    
    def publish_location(self,ride_id,location_data):
        self.redis_client.publish(f"ride_{ride_id}",json.dumps(location_data))

        threading.Thread(
            target=self._store_in_mongodb,
            args=(location_data,),
            daemon=True
        ).start()

    def _store_in_mongodb(self,location_data):
            """Background mogodb storage"""

            from .services import LiveLocationService

            try:
                 LiveLocationService.store_live_location(
                      location_data['driver_id'],
                      location_data['latitude'],
                      location_data['longitude']  
                 )

            except :
                 print(f'Mongodb storage error{location_data}')


    def subscribe_to_ride(self,ride_id,websocket_consumer):
            channel=f"ride_{ride_id}"
            if channel not in self.subscribers:
                self.subscribers[channel]=[]
            
            self.subscribers[channel].append(websocket_consumer)


    def unsubscribe_to_ride(self,ride_id,websocket_consumer):
         channel=f"ride_{ride_id}"

         if channel in self.subscribers:
              self.subscribers[channel].remove(websocket_consumer)


redis_manager=Redis_Manager()                  
