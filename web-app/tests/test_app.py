"""Module created to test the GoDutch Flask application"""

from app import app  # Flask instance of the API


def test_index_route():
    """Request the path '/' and ensure a 200 code response"""
    response = app.test_client().get("/")

    assert response.status_code == 200
