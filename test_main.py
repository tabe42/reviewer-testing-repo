import pytest
from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)

def test_health_check():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json() == {'status': 'OK'}


def test_create_user():
    new_user = {'name': 'John Doe', 'email': 'john@example.com', 'is_active': True}
    response = client.post('/users', json=new_user)
    assert response.status_code == 200
    assert 'id' in response.json()
    assert response.json()['name'] == new_user['name']
    assert response.json()['email'] == new_user['email']
    assert response.json()['is_active'] == new_user['is_active']


def test_get_user():
    new_user = {'name': 'Jane Doe', 'email': 'jane@example.com', 'is_active': False}
    response = client.post('/users', json=new_user)
    user_id = response.json()['id']
    response = client.get(f'/users/{user_id}')
    assert response.status_code == 200
    assert response.json() == new_user


def test_update_user():
    new_user = {'name': 'Update User', 'email': 'update@example.com', 'is_active': True}
    response = client.post('/users', json=new_user)
    user_id = response.json()['id']
    updated_user = {'name': 'Updated User', 'email': 'updated@example.com', 'is_active': False}
    response = client.put(f'/users/{user_id}', json=updated_user)
    assert response.status_code == 200
    assert response.json() == updated_user


def test_delete_user():
    new_user = {'name': 'Delete User', 'email': 'delete@example.com', 'is_active': True}
    response = client.post('/users', json=new_user)
    user_id = response.json()['id']
    response = client.delete(f'/users/{user_id}')
    assert response.status_code == 200
    assert response.json()['name'] == new_user['name']
    assert response.json()['email'] == new_user['email']
    assert response.json()['is_active'] == new_user['is_active']
