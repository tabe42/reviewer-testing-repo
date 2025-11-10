import pytest
from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)


def test_health_check():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}


def test_create_user():
    response = client.post('/users', json={"name": "John Doe", "email": "john.doe@example.com", "is_active": True})
    assert response.status_code == 201
    assert 'id' in response.json()
    assert response.json()['name'] == 'John Doe'
    assert response.json()['email'] == 'john.doe@example.com'
    assert response.json()['is_active'] is True


def test_get_user():
    response = client.post('/users', json={"name": "Jane Doe", "email": "jane.doe@example.com", "is_active": True})
    assert response.status_code == 201
    user_id = response.json()['id']
    
    response = client.get(f'/users/{user_id}')
    assert response.status_code == 200
    assert response.json()['id'] == user_id
    assert response.json()['name'] == 'Jane Doe'
    assert response.json()['email'] == 'jane.doe@example.com'
    assert response.json()['is_active'] is True


def test_update_user():
    response = client.post('/users', json={"name": "Alice", "email": "alice@example.com", "is_active": True})
    assert response.status_code == 201
    user_id = response.json()['id']
    
    response = client.put(f'/users/{user_id}', json={"name": "Alice Updated", "email": "alice.updated@example.com", "is_active": False})
    assert response.status_code == 200
    assert response.json()['id'] == user_id
    assert response.json()['name'] == 'Alice Updated'
    assert response.json()['email'] == 'alice.updated@example.com'
    assert response.json()['is_active'] is False


def test_delete_user():
    response = client.post('/users', json={"name": "Bob", "email": "bob@example.com", "is_active": True})
    assert response.status_code == 201
    user_id = response.json()['id']
    
    response = client.delete(f'/users/{user_id}')
    assert response.status_code == 200
    assert response.json() == {'message': 'User deleted'}

    response = client.get(f'/users/{user_id}')
    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}
