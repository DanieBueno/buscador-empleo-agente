from fastapi.testclient import TestClient
from ..main import app
from ..database import Base, engine

Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_create_product():
    response = client.post('/products/', json={'name': 'Test', 'description': 'Desc'})
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == 'Test'

def test_list_products():
    response = client.get('/products/')
    assert response.status_code == 200
    assert isinstance(response.json(), list)
