from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_scrape_endpoint():
    response = client.get("/scrape")
    assert response.status_code == 200
    assert "message" in response.json()
    assert isinstance(response.json()["scraped_quotes"], list)

def test_data_endpoint():
    response = client.get("/data")
    assert response.status_code == 200
    assert "data" in response.json()
