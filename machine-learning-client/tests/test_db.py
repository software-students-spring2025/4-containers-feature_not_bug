"""This module tests the ML client connection and interaction with the DB"""

import mongomock
import pytest

from db import store_receipt_text
from db import store_charge_per_person

shared_client = mongomock.MongoClient()
shared_db = shared_client["test_dutch_pay"]


def get_test_db():
    """ "Get test DB"""
    return shared_db


@pytest.fixture(autouse=True)
def patch_get_db(monkeypatch):
    """ "Monkeypatch to make sure that mock DB is injected during runtime"""
    monkeypatch.setattr("db.get_db", get_test_db)


def test_store_receipt_text():
    """Test storing the raw receipt text into DB"""
    sample_receipt_text = "BigMac 5.0\nLarge Coke 3.0\nChicken McNuggets 5.0\nSub-total   13.0\nTAX   2.0\nTotal   15.0" #pylint: disable=line-too-long

    inserted_id = store_receipt_text(sample_receipt_text)
    assert inserted_id is not None

    stored_doc = shared_db.receipts.find_one({"_id": inserted_id})
    assert stored_doc is not None
    assert stored_doc["receipt_text"] == sample_receipt_text


def test_store_charge_per_person_data_type():
    """Test that inserted document contains a dictionary under the 'charge_info' field"""
    sample_charge_info = {"Alice": 10.77, "Bob": 11.44, "Charlie": 10.77}
    inserted_id = store_charge_per_person(sample_charge_info)
    stored_doc = shared_db.receipts.find_one({"_id": inserted_id})
    assert isinstance(stored_doc["charge_info"], dict)


def test_store_charge_per_person_normal():
    """Test storing the charge per person in DB"""
    sample_charge_info = {"Alice": 10.77, "Bob": 11.44, "Charlie": 10.77}

    inserted_id = store_charge_per_person(sample_charge_info)
    assert inserted_id is not None

    stored_doc = shared_db.receipts.find_one({"_id": inserted_id})
    assert stored_doc is not None
    assert stored_doc["charge_info"] == sample_charge_info


def test_store_charge_per_person_empty():
    """Test that storing an empty charge per person in DB is correctly handled"""
    sample_charge_info = {}

    inserted_id = store_charge_per_person(sample_charge_info)
    assert inserted_id is not None

    stored_doc = shared_db.receipts.find_one({"_id": inserted_id})
    assert stored_doc is not None
    assert stored_doc["charge_info"] == sample_charge_info
