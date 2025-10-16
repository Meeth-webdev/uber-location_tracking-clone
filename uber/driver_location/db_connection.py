from pymongo import MongoClient
from django.conf import settings

def get_monogdb_connection():
    """
    Returns MongoDb connection to the server 
    """

    client=MongoClient(settings.MONGO_DB_URI)
    db=client[settings.MONGO_DB_NAME]
    return db 


class MongoDbConnection:
    _instance=None

    def __new__(cls):
        if cls._instance is None:
            cls._instance=super().__new__(cls)
            cls._instance.client=MongoClient(settings.MONGO_DB_URI)
            cls._instance.db=cls._instance.client[settings.MONGO_DB_NAME]

        return cls._instance


    def get_database(self):
        self.db