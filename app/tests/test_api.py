from fastapi.testclient import TestClient

from app.api import app


client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == (
        "Retail Sales & Inventory API is running"
    )


def test_kpis():
    response = client.get("/kpis")

    assert response.status_code == 200

    data = response.json()

    assert "orders" in data
    assert "units_sold" in data
    assert "revenue" in data
    assert "average_ticket" in data

    assert data["orders"] == 1500


def test_products():
    response = client.get("/products")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0

    assert "name" in data[0]
    assert "category" in data[0]
    assert "unit_price" in data[0]