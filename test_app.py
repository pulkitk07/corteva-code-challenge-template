import pytest
from app import app

def test_get_weather():
    with app.test_client() as client:
        response = client.get('/api')
        assert response.status_code == 200
