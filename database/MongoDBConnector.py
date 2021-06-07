import config as ENV
import dns
from pymongo import MongoClient

class MongoConnector:

    # """For connect MongoDB Database"""

    client = MongoClient(ENV.MONGODB_USER)
    dbname = client.get_database("UserDB")
  
    

    @classmethod
    def connect(cls) -> MongoClient:
        print("Mongodb:=> connected!")
        return cls.dbname

    @classmethod
    def disconnect(cls):
        print("Mongodb:=> disconnected!")
        return cls.client.close()
