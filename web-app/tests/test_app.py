"""Module created to test the GoDutch Flask application"""

import pytest
from app import app_setup  # Flask instance of the API


@pytest.fixture
def client():
    """
    Create and yield Flask app
    """
    app = app_setup()
    app.testing = True  # necessary for assertions to work correctly
    with app.test_client() as client:
        yield client


def test_index_route(client):
    """Request the path '/' and ensure a 200 code response"""
    response = client.get("/")

    assert response.status_code == 200
