from fastapi.testclient import TestClient
from fastapi import FastAPI
from main import app
import pytest
import json

client = TestClient(app)

def test_health_check():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}

def test_get_users():
    response = client.get('/users/')
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_user():
    response = client.get('/users/1')
    assert response.status_code == 404

def test_create_user():
    response = client.post('/users/', json={'name': 'John Doe', 'email': 'john.doe@example.com', 'is_active': True})
    assert response.status_code == 200
    assert response.json()['name'] == 'John Doe'

def test_update_user():
    client.post('/users/', json={'name': 'John Doe', 'email': 'john.doe@example.com', 'is_active': True})
    response = client.put('/users/1', json={'name': 'Updated John Doe', 'email': 'updated.john.doe@example.com', 'is_active': False})
    assert response.status_code == 200
    assert response.json()['name'] == 'Updated John Doe'

def test_delete_user():
    client.post('/users/', json={'name': 'John Doe', 'email': 'john.doe@example.com', 'is_active': True})
    response = client.delete('/users/1')
    assert response.status_code == 200
    assert response.json() == {'message': 'User deleted'}