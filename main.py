from typing import List, Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import json

app = FastAPI()

DB_FILE = 'users_db.json'

class User(BaseModel):
    id: int = Field(..., example=1)
    name: str = Field(..., example='John Doe')
    email: str = Field(..., example='john.doe@example.com')
    is_active: bool = Field(..., example=True)

def load_db() -> List[Dict]:
    try:
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        with open(DB_FILE, 'w') as f:
            json.dump([], f)
        return []

def save_db(data: List[Dict]):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f)

def get_next_id(db: List[Dict]) -> int:
    return (max([user['id'] for user in db], default=0) + 1) if db else 1

@app.get('/health')
def health_check():
    return {'status': 'ok'}


@app.post('/users/', response_model=User)
def create_user(user: User):
    db = load_db()
    user.id = get_next_id(db)
    db.append(user.dict())
    save_db(db)
    return user


@app.get('/users/{user_id}', response_model=User)
def get_user(user_id: int):
    db = load_db()
    for user in db:
        if user['id'] == user_id:
            return User(**user)
    raise HTTPException(status_code=404, detail='User not found')


@app.put('/users/{user_id}', response_model=User)
def update_user(user_id: int, user: User):
    db = load_db()
    for i, existing_user in enumerate(db):
        if existing_user['id'] == user_id:
            user.id = existing_user['id']
            db[i] = user.dict()
            save_db(db)
            return user
    raise HTTPException(status_code=404, detail='User not found')


@app.delete('/users/{user_id}')
def delete_user(user_id: int):
    db = load_db()
    for i, user in enumerate(db):
        if user['id'] == user_id:
            del db[i]
            save_db(db)
            return {'message': 'User deleted'}
    raise HTTPException(status_code=404, detail='User not found')