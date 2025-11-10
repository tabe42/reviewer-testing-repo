from typing import List, Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import json

app = FastAPI()

# File path for the database
DB_FILE = 'users_db.json'

# Helper functions
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
    return max((user['id'] for user in db), default=0) + 1


# Pydantic model for User
class User(BaseModel):
    id: int = Field(..., alias='id')
    name: str = Field(..., alias='name')
    email: str = Field(..., alias='email')
    is_active: bool = Field(..., alias='is_active')


@app.get('/health')
def health_check():
    return {'status': 'ok'}


@app.get('/users/{user_id}', response_model=User)
def get_user(user_id: int):
    db = load_db()
    for user in db:
        if user['id'] == user_id:
            return user
    raise HTTPException(status_code=404, detail='User not found')


@app.post('/users', response_model=User)
def create_user(user: User):
    db = load_db()
    user_dict = user.dict()
    user_dict['id'] = get_next_id(db)
    db.append(user_dict)
    save_db(db)
    return user_dict


@app.put('/users/{user_id}', response_model=User)
def update_user(user_id: int, user: User):
    db = load_db()
    for idx, existing_user in enumerate(db):
        if existing_user['id'] == user_id:
            db[idx] = user.dict()
            db[idx]['id'] = user_id
            save_db(db)
            return db[idx]
    raise HTTPException(status_code=404, detail='User not found')


@app.delete('/users/{user_id}')
def delete_user(user_id: int):
    db = load_db()
    for idx, existing_user in enumerate(db):
        if existing_user['id'] == user_id:
            del db[idx]
            save_db(db)
            return {'message': 'User deleted'}
    raise HTTPException(status_code=404, detail='User not found')