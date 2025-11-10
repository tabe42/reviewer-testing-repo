from fastapi.testclient import TestClient
from main import app
import pytest
import json

client = TestClient(app)

# Helper function to load the database
def load_db():
    with open('users_db.json', 'r') as file:
        return json.load(file)

def test_health_check():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}

def test_create_user():
    response = client.post('/users', json={"name": "John Doe", "email": "john@example.com", "is_active": True})
    assert response.status_code == 201
    assert 'id' in response.json()
    assert response.json()['name'] == 'John Doe'

def test_get_user():
    # Create a user to fetch
    client.post('/users', json={"name": "Alice", "email": "alice@example.com", "is_active": True})
    response = client.get('/users/1')
    assert response.status_code == 200
    assert response.json()['name'] == 'Alice'

def test_update_user():
    # Create a user to update
    client.post('/users', json={"name": "Bob", "email": "bob@example.com", "is_active": True})
    response = client.put('/users/1', json={"name": "Bobby", "email": "bobby@example.com", "is_active": False})
    assert response.status_code == 200
    assert response.json()['name'] == 'Bobby'
    assert response.json()['is_active'] == False

def test_delete_user():
    # Create a user to delete
    client.post('/users', json={"name": "Charlie", "email": "charlie@example.com", "is_active": True})
    response = client.delete('/users/1')
    assert response.status_code == 204
    db = load_db()
    assert len(db) == 0
