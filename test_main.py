from fastapi.testclient import TestClient
from main import app
import pytest
import json

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {'status': 'OK'}


def test_create_user():
    response = client.post("/users/", json={"name": "John Doe", "email": "john.doe@example.com", "is_active": True})
    assert response.status_code == 200
    assert 'id' in response.json()
    assert response.json()['name'] == "John Doe"


def test_read_user():
    # First, create a user
    create_response = client.post("/users/", json={"name": "Alice", "email": "alice@example.com", "is_active": True})
    user_id = create_response.json()['id']

    # Then, read the user
    read_response = client.get(f"/users/{user_id}")
    assert read_response.status_code == 200
    assert read_response.json()['name'] == "Alice"


def test_update_user():
    # First, create a user
    create_response = client.post("/users/", json={"name": "Bob", "email": "bob@example.com", "is_active": True})
    user_id = create_response.json()['id']

    # Then, update the user
    update_response = client.put(f"/users/{user_id}", json={"name": "Bobby", "email": "bobby@example.com", "is_active": False})
    assert update_response.status_code == 200
    assert update_response.json()['name'] == "Bobby"


def test_delete_user():
    # First, create a user
    create_response = client.post("/users/", json={"name": "Charlie", "email": "charlie@example.com", "is_active": True})
    user_id = create_response.json()['id']

    # Then, delete the user
    delete_response = client.delete(f"/users/{user_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {'message': 'User deleted'}


def test_read_non_existing_user():
    response = client.get("/users/999")
    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}


def test_update_non_existing_user():
    response = client.put("/users/999", json={"name": "Non Existing", "email": "nonexisting@example.com", "is_active": True})
    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}


def test_delete_non_existing_user():
    response = client.delete("/users/999")
    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}
