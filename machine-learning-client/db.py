"""
This module stores information received or processed by the ML-client analyzer
in the DB
"""

import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
uri = os.getenv("MONGO_URI")
client = MongoClient(uri)
db_name = os.getenv("MONGO_DBNAME")


def get_db():
    """Get DB connection"""
    return client[db_name]


def store_receipt_info(receipt_text, charge_per_person):
    """Store raw receipt text and charge per person info in DB"""
    db = get_db()

    receipt_info = {
        "receipt_text": receipt_text,
        "charge_info": charge_per_person,
    }
    result = db.receipts.insert_one(receipt_info)
    return result.inserted_id
