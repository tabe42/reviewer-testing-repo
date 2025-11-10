from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)

def test_health_check():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json() == {'status': 'OK'}

def test_create_user():
    response = client.post('/users', json={"name": "John Doe", "email": "john.doe@example.com", "is_active": True})
    assert response.status_code == 200
    user = response.json()
    assert 'id' in user
    assert user['name'] == 'John Doe'
    assert user['email'] == 'john.doe@example.com'
    assert user['is_active'] is True

def test_get_users():
    client.post('/users', json={"name": "Jane Doe", "email": "jane.doe@example.com", "is_active": False})
    response = client.get('/users')
    assert response.status_code == 200
    users = response.json()
    assert len(users) >= 1

def test_get_user():
    response = client.post('/users', json={"name": "Alice", "email": "alice@example.com", "is_active": True})
    user = response.json()
    user_id = user['id']
    response = client.get(f'/users/{user_id}')
    assert response.status_code == 200
    assert response.json() == user

def test_update_user():
    response = client.post('/users', json={"name": "Bob", "email": "bob@example.com", "is_active": True})
    user = response.json()
    user_id = user['id']
    response = client.put(f'/users/{user_id}', json={"name": "Bobby", "email": "bobby@example.com", "is_active": False})
    assert response.status_code == 200
    updated_user = response.json()
    assert updated_user['name'] == 'Bobby'
    assert updated_user['email'] == 'bobby@example.com'
    assert updated_user['is_active'] is False

def test_delete_user():
    response = client.post('/users', json={"name": "Charlie", "email": "charlie@example.com", "is_active": True})
    user = response.json()
    user_id = user['id']
    response = client.delete(f'/users/{user_id}')
    assert response.status_code == 200
    assert response.json() == {'message': 'User deleted'}
    response = client.get(f'/users/{user_id}')
    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}
