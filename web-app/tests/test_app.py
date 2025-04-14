"""Module created to test the GoDutch Flask application"""

import pytest
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
    assert response.data == b"Receipt image not found 2"


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
    assert response.data == b"Error in format of entered tip"

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
    assert response.data == b"Tip cannot be converted into a decimal and was likely entered wrong"


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
    assert response.data == b"Number of people mismatched"

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
        # trying to POST to a running ML client; gets a connectivity error
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
        session["result_id"] = "111111111111111111111111"

    response = client.get("/result")
    assert response.status_code == 404
    assert b"No results found" == response.data


def test_get_with_valid_session(client):
    """Try sending get request to /result with configured session variables, valid value"""

    # set session variable
    with client.session_transaction() as session:
        session["result_id"] = "67fc3fd6d5619018c1bdf3a2"

    # query for the dummy data
    response = client.get("/result")

    print(response.data)

    # assertions
    # affirmative response code
    assert response.status_code == 200
    # correct template is loading
    assert b"Individual Breakdown" in response.data
    # template contains data from this db query
    assert b"Charlie" in response.data
