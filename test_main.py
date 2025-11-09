from fastapi.testclient import TestClient
from main import app
import pytest
import json

client = TestClient(app)


def test_health_check():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json() == {'status': 'OK'}


def test_get_users():
    response = client.get('/users/')
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_user_not_found():
    response = client.get('/users/1')
    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}


def test_create_user():
    user_data = {
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'is_active': True
    }
    response = client.post('/users/', json=user_data)
    assert response.status_code == 200
    assert response.json()['name'] == 'John Doe'


def test_update_user():
    user_data = {
        'id': 1,
        'name': 'John Doe Updated',
        'email': 'john.doe.updated@example.com',
        'is_active': False
    }
    response = client.put('/users/1', json=user_data)
    assert response.status_code == 200
    assert response.json()['name'] == 'John Doe Updated'


def test_delete_user():
    response = client.delete('/users/1')
    assert response.status_code == 200
    assert response.json() == {'message': 'User deleted'}


def test_update_user_not_found():
    user_data = {
        'id': 2,
        'name': 'John Doe Updated',
        'email': 'john.doe.updated@example.com',
        'is_active': False
    }
    response = client.put('/users/2', json=user_data)
    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}
