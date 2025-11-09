import pytest
from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {'status': 'OK'}

def test_create_user():
    new_user = {
        'name': 'John Doe',
        'email': 'john@example.com',
        'is_active': True
    }
    response = client.post("/users/", json=new_user)
    assert response.status_code == 200
    assert response.json()['name'] == new_user['name']
    assert response.json()['email'] == new_user['email']
    assert response.json()['is_active'] == new_user['is_active']

def test_get_users():
    response = client.get("/users/")
    assert response.status_code == 200

def test_get_user_not_found():
    response = client.get("/users/999")
    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}

def test_update_user():
    new_user = {
        'name': 'John Doe',
        'email': 'john@example.com',
        'is_active': True
    }
    response = client.post("/users/", json=new_user)
    user_id = response.json()['id']
    updated_user = {
        'name': 'Jane Doe',
        'email': 'jane@example.com',
        'is_active': False
    }
    response = client.put(f"/users/{user_id}/", json=updated_user)
    assert response.status_code == 200
    assert response.json()['name'] == updated_user['name']
    assert response.json()['email'] == updated_user['email']
    assert response.json()['is_active'] == updated_user['is_active']

def test_delete_user():
    new_user = {
        'name': 'John Doe',
        'email': 'john@example.com',
        'is_active': True
    }
    response = client.post("/users/", json=new_user)
    user_id = response.json()['id']
    response = client.delete(f"/users/{user_id}/")
    assert response.status_code == 200
    assert response.json()['id'] == user_id
