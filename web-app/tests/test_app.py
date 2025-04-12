"""Module created to test the GoDutch Flask application"""

import pytest
from app import app_setup  # Flask instance of the API
from requests.exceptions import ConnectionError


@pytest.fixture(name="client")
def fixture_client():
    """
    Create and yield Flask app
    """
    app = app_setup()
    app.testing = True  # necessary for assertions to work correctly
    with app.test_client() as testing_client:
        yield testing_client


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

    data_with_errors = dict({
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
    })

    response = client.post("/upload", data=data_with_errors)
    assert response.status_code == 400


def test_error_tip(client):
    """Try sending erroneous post requests -- tip with too many decimal points, too many digits"""

    data_with_errors = dict({
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
    })

    response = client.post("/upload", data=data_with_errors)
    assert response.status_code == 400

    data_with_errors = dict({
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
    })

    response = client.post("/upload", data=data_with_errors)
    assert response.status_code == 400


def test_error_num_people(client):
    """Try sending erroneous post requests -- num people mismatched with descriptions"""

    data_with_errors = dict({
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
    })

    response = client.post("/upload", data=data_with_errors)
    assert response.status_code == 400

    data_with_errors = dict({
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
    })

    response = client.post("/upload", data=data_with_errors)
    assert response.status_code == 400


def test_correct_post(client):
    """Try sending correct post"""

    data = dict({
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
    })

    try: 
        response = client.post("/upload", data=data)
    except ConnectionError as e:
        assert True
    else:
        assert False
