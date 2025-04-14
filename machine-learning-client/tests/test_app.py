"""Module created to test the ML client Flask server API"""

import pytest
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
    assert b"running" in response.data


def test_correct_post(client):
    """Try sending correct post"""

    files = {
        "receipt": (
            "fake",
            "fake",
            "fake",
        )
    }
    data = dict(
        {
            "tip": "17.17",
            "num-people": 4,
            "person-1-name": "jane",
            "person-1-items": "chicken, coke",
            "person-2-name": "joe",
            "person-2-items": "pesto pasta",
            "person-3-name": "john",
            "person-3-items": "calamari, coke",
            "person-4-name": "jack",
            "person-4-items": "bread",
        }
    )

    response = client.post("/submit", data=data)
    assert response.status_code == 400
    assert b"receipt not provided in files" == response.data
