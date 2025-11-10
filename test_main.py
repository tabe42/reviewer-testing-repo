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
    response = client.post('/users', json={'name': 'John Doe', 'email': 'john@example.com', 'is_active': True})
    assert response.status_code == 200
    assert response.json()['name'] == 'John Doe'


def test_get_user():
    # Create a user first
    client.post('/users', json={'name': 'Jane Doe', 'email': 'jane@example.com', 'is_active': True})
    
    # Get the user
    response = client.get('/users/1')
    assert response.status_code == 200
    assert response.json()['name'] == 'Jane Doe'


def test_update_user():
    # Create a user first
    client.post('/users', json={'name': 'Alice', 'email': 'alice@example.com', 'is_active': True})
    
    # Update the user
    response = client.put('/users/1', json={'name': 'Alice Updated', 'email': 'alice_updated@example.com', 'is_active': False})
    assert response.status_code == 200
    assert response.json()['name'] == 'Alice Updated'


def test_delete_user():
    # Create a user first
    client.post('/users', json={'name': 'Bob', 'email': 'bob@example.com', 'is_active': True})
    
    # Delete the user
    response = client.delete('/users/1')
    assert response.status_code == 200
    assert response.json() == {'message': 'User deleted'}


def test_get_user_not_found():
    response = client.get('/users/999')
    assert response.status_code == 404
    assert response.json()['detail'] == 'User not found'


def test_update_user_not_found():
    response = client.put('/users/999', json={'name': 'New Name', 'email': 'new@example.com', 'is_active': False})
    assert response.status_code == 404
    assert response.json()['detail'] == 'User not found'


def test_delete_user_not_found():
    response = client.delete('/users/999')
    assert response.status_code == 404
    assert response.json()['detail'] == 'User not found'
