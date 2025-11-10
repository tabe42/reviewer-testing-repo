from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)


def test_health_check():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}


def test_create_user():
    response = client.post('/users/', json={
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'is_active': True
    })
    assert response.status_code == 200
    assert 'id' in response.json()


def test_get_user():
    user_id = 1
    response = client.get(f'/users/{user_id}')
    assert response.status_code == 200
    assert response.json()['id'] == user_id


def test_update_user():
    user_id = 1
    response = client.put(f'/users/{user_id}', json={
        'name': 'Jane Doe',
        'email': 'jane.doe@example.com',
        'is_active': False
    })
    assert response.status_code == 200
    assert response.json()['name'] == 'Jane Doe'


def test_delete_user():
    user_id = 1
    response = client.delete(f'/users/{user_id}')
    assert response.status_code == 200
    assert response.json() == {'message': 'User deleted'}


def test_get_user_not_found():
    response = client.get('/users/999')
    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}


def test_update_user_not_found():
    response = client.put('/users/999', json={
        'name': 'Jane Doe',
        'email': 'jane.doe@example.com',
        'is_active': False
    })
    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}


def test_delete_user_not_found():
    response = client.delete('/users/999')
    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}