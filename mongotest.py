import pymongo
from decouple import config

client = pymongo.MongoClient(config("MONGO_CONNECTION"))
db = client['sample_training']

collection = db['grades']

a = collection.find_one({"student_id": 0})

print(a)
