from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)

def test_healthcheck():
    response = client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}

def test_create_user():
    response = client.post("/users", json={"name": "John Doe", "email": "john.doe@example.com", "is_active": True})
    assert response.status_code == 201
    assert 'id' in response.json()

def test_get_user():
    # Create a user first
    create_response = client.post("/users", json={"name": "Jane Doe", "email": "jane.doe@example.com", "is_active": True})
    user_id = create_response.json()['id']
    
    # Get the user
    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 200
    assert get_response.json()['name'] == "Jane Doe"

def test_update_user():
    # Create a user first
    create_response = client.post("/users", json={"name": "Alice", "email": "alice@example.com", "is_active": True})
    user_id = create_response.json()['id']
    
    # Update the user
    update_response = client.put(f"/users/{user_id}", json={"name": "Alice Updated", "email": "alice.updated@example.com", "is_active": False})
    assert update_response.status_code == 200
    assert update_response.json()['name'] == "Alice Updated"

def test_delete_user():
    # Create a user first
    create_response = client.post("/users", json={"name": "Bob", "email": "bob@example.com", "is_active": True})
    user_id = create_response.json()['id']
    
    # Delete the user
    delete_response = client.delete(f"/users/{user_id}")
    assert delete_response.status_code == 204
