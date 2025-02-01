import sys
import os

# Add project root to PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from app import create_app
from flask_jwt_extended import create_access_token

@pytest.fixture
def client():
    """ Creates a test client for the Flask app """
    app = create_app()
    app.config["TESTING"] = True  # Enables Flask test mode
    with app.test_client() as client:
        yield client

@pytest.fixture
def auth_headers():
    """ Creates authentication headers for an admin user """
    access_token = create_access_token(identity="admin")
    return {"Authorization": f"Bearer {access_token}"}
