from pymongo import MongoClient
from google.colab import userdata

MONGODB_URI = userdata.get("MONGODB_URI")

mongo_conn = MongoClient(MONGODB_URI)
MONGODB_DATABASE="synqanun"

db_client = mongo_conn[MONGODB_DATABASE]

collection = db_client["legal_chunks"]
def insert_many(full_chunks):
  result = collection.insert_many(full_chunks)
  print("Inserted:", len(result.inserted_ids))

