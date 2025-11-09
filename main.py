from fastapi import FastAPI, HTTPException
from typing import List, Dict
import json

app = FastAPI()


def load_db() -> List[Dict]:
    try:
        with open('users_db.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        with open('users_db.json', 'w') as f:
            json.dump([], f)
        return []


def save_db(data: List[Dict]):
    with open('users_db.json', 'w') as f:
        json.dump(data, f)


def get_next_id(db: List[Dict]) -> int:
    return max((user['id'] for user in db), default=0) + 1


@app.get('/health')
def health_check():
    return {'status': 'ok'}


@app.get('/users/', response_model=List[Dict])
def get_users():
    db = load_db()
    return db


@app.get('/users/{user_id}', response_model=Dict)
def get_user(user_id: int):
    db = load_db()
    user = next((user for user in db if user['id'] == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user


@app.post('/users/', response_model=Dict)
def create_user(user: Dict):
    db = load_db()
    user_id = get_next_id(db)
    user['id'] = user_id
    db.append(user)
    save_db(db)
    return user


@app.put('/users/{user_id}', response_model=Dict)
def update_user(user_id: int, user: Dict):
    db = load_db()
    for i, existing_user in enumerate(db):
        if existing_user['id'] == user_id:
            user['id'] = existing_user['id']
            db[i] = user
            save_db(db)
            return user
    raise HTTPException(status_code=404, detail='User not found')


@app.delete('/users/{user_id}', response_model=Dict)
def delete_user(user_id: int):
    db = load_db()
    for i, existing_user in enumerate(db):
        if existing_user['id'] == user_id:
            removed_user = db.pop(i)
            save_db(db)
            return removed_user
    raise HTTPException(status_code=404, detail='User not found')
