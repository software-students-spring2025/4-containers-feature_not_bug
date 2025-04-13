"""
This module stores information received or processed by the ML-client analyzer
in the DB
"""

import os
from pymongo import MongoClient
from dotenv import load_dotenv


def get_db():
    """Get DB connection"""
    load_dotenv()
    uri = os.getenv("MONGO_URI")
    client = MongoClient(uri)
    db_name = os.getenv("MONGO_DBNAME")

    return client[db_name]


def store_receipt_text(receipt_text):
    """Store raw receipt text in DB"""
    db = get_db()

    result = db.receipts.insert_one({"receipt_text": receipt_text})
    return result.inserted_id


def store_charge_per_person(charge_per_person):
    """Store charge per person info in DB"""
    db = get_db()

    result = db.receipts.insert_one({"charge_info": charge_per_person})
    return result.inserted_id
