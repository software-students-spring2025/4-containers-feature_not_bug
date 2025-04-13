import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
uri = os.getenv("MONGO_URI")
client = MongoClient(uri)
db_name = os.getenv("MONGO_DBNAME")


result = client[db_name].receipts.insert_one({"receipt_text": "this is dummy text - this entry in the database is false, used purely for pytest."})
print(result.inserted_id)