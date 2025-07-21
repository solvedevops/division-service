import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "division-service"}

def test_division_success():
    """Test successful division operation."""
    response = client.get("/?first_number=10&second_number=2")
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == 5.0
    assert data["operation"] == "division"
    assert data["first_number"] == 10.0
    assert data["second_number"] == 2.0

def test_division_with_decimals():
    """Test division with decimal numbers."""
    response = client.get("/?first_number=7.5&second_number=2.5")
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == 3.0

def test_division_by_zero():
    """Test division by zero returns error."""
    response = client.get("/?first_number=10&second_number=0")
    assert response.status_code == 400
    assert "Cannot divide by zero" in response.json()["detail"]

def test_division_negative_numbers():
    """Test division with negative numbers."""
    response = client.get("/?first_number=-10&second_number=2")
    assert response.status_code == 200
    assert response.json()["result"] == -5.0

def test_division_default_values():
    """Test division with default values (0/0)."""
    response = client.get("/")
    assert response.status_code == 400
    assert "Cannot divide by zero" in response.json()["detail"]