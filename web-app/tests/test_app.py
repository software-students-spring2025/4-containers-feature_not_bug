"""Module created to test the GoDutch Flask application"""

import pytest
import os
import certifi
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
# from bson.objectid import ObjectId
from requests.exceptions import ConnectionError as conn_err
from app import app_setup  # Flask instance of the API


@pytest.fixture(name="client")
def fixture_client():
    """
    Create and yield Flask app
    """
    app = app_setup()
    app.testing = True  # necessary for assertions to work correctly
    with app.test_client() as testing_client:
        yield testing_client


@pytest.fixture(name="db")
def fixture_db():
    """
    Connect to the MongoDB database
    """
    uri = os.getenv("MONGO_URI")
    mongo = MongoClient(uri, server_api=ServerApi("1"), tlsCAFile=certifi.where())
    dbname = os.getenv("MONGO_DB", "dutch_pay")

    # Get DB connection
    db = mongo[dbname]
    yield db


def test_index_route(client):
    """Request the path '/' and ensure a 200 code response"""
    response = client.get("/")

    assert response.status_code == 200


def test_index_contains_text(client):
    """Ensure that the page contains expected text"""
    response = client.get("/")
    assert b"GoDutch" in response.data


def test_error_bad_receipt(client):
    """Try sending erroneous post requests -- empty receipts"""

    data_with_errors = dict(
        {
            "upload-receipt": "",
            "capture-receipt": "",
            "tip": "17.17",
            "num-people": 4,
            "person-1-name": "jane",
            "person-1-desc": "chicken, coke",
            "person-2-name": "joe",
            "person-2-desc": "pesto pasta",
            "person-3-name": "john",
            "person-3-desc": "calamari, coke",
            "person-4-name": "jack",
            "person-4-desc": "bread",
        }
    )

    response = client.post("/upload", data=data_with_errors)
    assert response.status_code == 400


def test_error_tip(client):
    """Try sending erroneous post requests -- tip with too many decimal points, too many digits"""

    data_with_errors = dict(
        {
            "upload-receipt": "",
            "capture-receipt": "sample.jpg",
            "tip": "17.111117",
            "num-people": 4,
            "person-1-name": "jane",
            "person-1-desc": "chicken, coke",
            "person-2-name": "joe",
            "person-2-desc": "pesto pasta",
            "person-3-name": "john",
            "person-3-desc": "calamari, coke",
            "person-4-name": "jack",
            "person-4-desc": "bread",
        }
    )

    response = client.post("/upload", data=data_with_errors)
    assert response.status_code == 400

    data_with_errors = dict(
        {
            "upload-receipt": "",
            "capture-receipt": "sample.jpg",
            "tip": "17.11.11",
            "num-people": 4,
            "person-1-name": "jane",
            "person-1-desc": "chicken, coke",
            "person-2-name": "joe",
            "person-2-desc": "pesto pasta",
            "person-3-name": "john",
            "person-3-desc": "calamari, coke",
            "person-4-name": "jack",
            "person-4-desc": "bread",
        }
    )

    response = client.post("/upload", data=data_with_errors)
    assert response.status_code == 400


def test_error_num_people(client):
    """Try sending erroneous post requests -- num people mismatched with descriptions"""

    data_with_errors = dict(
        {
            "upload-receipt": "",
            "capture-receipt": "sample.jpg",
            "tip": "17.17",
            "num-people": 4,
            "person-1-name": "jane",
            "person-1-desc": "chicken, coke",
            "person-2-name": "joe",
            "person-2-desc": "pesto pasta",
            "person-3-name": "john",
            "person-3-desc": "calamari, coke",
        }
    )

    response = client.post("/upload", data=data_with_errors)
    assert response.status_code == 400

    data_with_errors = dict(
        {
            "upload-receipt": "",
            "capture-receipt": "sample.jpg",
            "tip": "17.17",
            "num-people": 4,
            "person-1-name": "jane",
            "person-1-desc": "chicken, coke",
            "person-2-name": "joe",
            "person-2-desc": "pesto pasta",
            "person-3-name": "john",
            "person-3-desc": "calamari, coke",
            "person-4-name": "jack",
            "person-4-desc": "bread",
            "person-5-name": "jack",
            "person-5-desc": "bread",
        }
    )

    response = client.post("/upload", data=data_with_errors)
    assert response.status_code == 400


def test_correct_post(client):
    """Try sending correct post"""

    data = dict(
        {
            "upload-receipt": "",
            "capture-receipt": "sample.jpg",
            "tip": "17.17",
            "num-people": 4,
            "person-1-name": "jane",
            "person-1-desc": "chicken, coke",
            "person-2-name": "joe",
            "person-2-desc": "pesto pasta",
            "person-3-name": "john",
            "person-3-desc": "calamari, coke",
            "person-4-name": "jack",
            "person-4-desc": "bread",
        }
    )

    try:
        response = client.post("/upload", data=data)
    except conn_err:
        assert True
    else:
        assert response.status_code == 400


def test_get_no_session(client):
    """Try sending get request to /result with no configured session variables"""

    response = client.get("/result")
    assert response.status_code == 400
    assert response.data == b"No result_id found in session"


def test_get_with_invalid_session(client):
    """Try sending get request to /result with configured session variables, but invalid value"""

    with client.session_transaction() as session:
        session["result_id"] = "67bd4bec5fc8bed996c3671d"

    response = client.get("/result")
    assert response.status_code == 404
    assert b"No results found" == response.data

""" 
def test_get_with_valid_session(client, db):
    ""Try sending get request to /result with configured session variables, valid value""

    # add dummy entry to database
    db_name = os.getenv("MONGO_DBNAME")
    result = db[db_name].receipts.insert_one({"receipt_text": "this is dummy text - this entry in the database is false, used purely for pytest."})
    
    # set session variable
    with client.session_transaction() as session:
        session["result_id"] = result.inserted_id

    # query for the dummy data
    response = client.get("/result")

    # cleanup 
    db[db_name].receipts.deleteOne({"inserted_id"})

    # assertions
    assert response.status_code == 200
    assert b"Individual Breakdown" in response.data


 """