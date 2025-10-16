from .db_connection import MongoDbConnection
from datetime import datetime

class LiveLocationService():
    @staticmethod
    def store_live_location(driver_id,latitude,longitude):
        db= MongoDbConnection.get_database()

        location_data={
            'driver_id':driver_id,
            'longitude':longitude,
            'latitude':latitude,
            'timestamp':datetime.utcnow(),
            'vehicle_speed':0,
            'heading':0
        }

        result= db.live_location.insertOne(location_data)


        from .models import User,DriverLocation
        driver= User.objects.get(id=driver_id)
        DriverLocation.objects.update_or_create(
            driver=driver,
            defaults={
                'latitude':latitude,
                'longitude':longitude
            }
        )

        return result.inserted_id
    

    @staticmethod
    def get_recent_locations(driver_id, limit=50):
        """Get recent location history for a driver"""
        db = MongoDbConnection().get_database()
        
        locations = db.live_locations.find(
            {'driver_id': driver_id}
        ).sort('timestamp', -1).limit(limit)
        
        return list(locations)
    
    @staticmethod
    def get_current_location(driver_id):
        """Get the most recent location of a driver"""
        db = MongoDbConnection().get_database()
        
        location = db.live_locations.find_one(
            {'driver_id': driver_id},
            sort=[('timestamp', -1)]
        )
        
        return location
