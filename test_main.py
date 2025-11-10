from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)

def test_health_check():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json() == {'status': 'OK'}

def test_create_user():
    new_user = {'name': 'John Doe', 'email': 'john.doe@example.com', 'is_active': True}
    response = client.post('/users', json=new_user)
    assert response.status_code == 201
    user_data = response.json()
    assert user_data['name'] == new_user['name']
    assert user_data['email'] == new_user['email']
    assert user_data['is_active'] == new_user['is_active']

def test_get_user():
    new_user = {'name': 'Jane Doe', 'email': 'jane.doe@example.com', 'is_active': False}
    response = client.post('/users', json=new_user)
    assert response.status_code == 201
    user_data = response.json()
    user_id = user_data['id']
    response = client.get(f'/users/{user_id}')
    assert response.status_code == 200
    assert response.json() == user_data

def test_update_user():
    new_user = {'name': 'Alice', 'email': 'alice@example.com', 'is_active': True}
    response = client.post('/users', json=new_user)
    assert response.status_code == 201
    user_data = response.json()
    user_id = user_data['id']
    updated_user = {'name': 'Alice Updated', 'email': 'alice.updated@example.com', 'is_active': False}
    response = client.put(f'/users/{user_id}', json=updated_user)
    assert response.status_code == 200
    assert response.json()['name'] == updated_user['name']
    assert response.json()['email'] == updated_user['email']
    assert response.json()['is_active'] == updated_user['is_active']

def test_delete_user():
    new_user = {'name': 'Bob', 'email': 'bob@example.com', 'is_active': True}
    response = client.post('/users', json=new_user)
    assert response.status_code == 201
    user_data = response.json()
    user_id = user_data['id']
    response = client.delete(f'/users/{user_id}')
    assert response.status_code == 204
    response = client.get(f'/users/{user_id}')
    assert response.status_code == 404
