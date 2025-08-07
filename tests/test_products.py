from fastapi.testclient import TestClient

def test_read_products_empty(client: TestClient):
    """
    Test reading products when the database is empty.
    """
    response = client.get("/api/v1/products/")
    assert response.status_code == 200
    assert response.json() == []

def test_read_categories_empty(client: TestClient):
    """
    Test reading categories when the database is empty.
    """
    response = client.get("/api/v1/categories/")
    assert response.status_code == 200
    assert response.json() == []
