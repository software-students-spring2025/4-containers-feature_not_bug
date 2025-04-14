"""This module tests the ML client connection and interaction with the DB"""

import mongomock
import pytest

from db import store_receipt_info

shared_client = mongomock.MongoClient()
shared_db = shared_client["test_dutch_pay"]


def get_test_db():
    """ "Get test DB"""
    return shared_db


@pytest.fixture(autouse=True)
def patch_get_db(monkeypatch):
    """ "Monkeypatch to make sure that mock DB is injected during runtime"""
    monkeypatch.setattr("db.get_db", get_test_db)


def test_store_receipt_info_success():
    """Test that store_receipt_data inserts a document with both fields"""
    sample_receipt_text = "BigMac 5.0\nLarge Coke 3.0\nReceipt details..."
    sample_charge_info = {"Alice": 10.77, "Bob": 11.44, "Charlie": 10.77}

    inserted_id = store_receipt_info(sample_receipt_text, sample_charge_info)
    assert inserted_id is not None

    stored_doc = shared_db.receipts.find_one({"_id": inserted_id})
    assert stored_doc is not None

    assert stored_doc.get("receipt_text") == sample_receipt_text
    assert stored_doc.get("charge_info") == sample_charge_info


def test_store_receipt_data_empty_values():
    """Test that storing with empty values still creates the proper document"""
    sample_receipt_text = ""
    sample_charge_info = {}

    inserted_id = store_receipt_info(sample_receipt_text, sample_charge_info)
    assert inserted_id is not None

    stored_doc = shared_db.receipts.find_one({"_id": inserted_id})
    assert stored_doc is not None

    assert stored_doc.get("receipt_text") == sample_receipt_text
    assert stored_doc.get("charge_info") == sample_charge_info
