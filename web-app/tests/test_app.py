"""Module created to test the GoDutch Flask application"""

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
    assert b"GoDutch" in response.data