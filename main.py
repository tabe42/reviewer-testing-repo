from typing import List, Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import json

app = FastAPI()

# Helper Functions

def load_db() -> List[Dict]:
    try:
        with open('users_db.json', 'r') as file:
            db = json.load(file)
    except FileNotFoundError:
        with open('users_db.json', 'w') as file:
            json.dump([], file)
        db = []
    return db

def save_db(data: List[Dict]):
    with open('users_db.json', 'w') as file:
        json.dump(data, file)

def get_next_id(db: List[Dict]) -> int:
    if db:
        return max(user['id'] for user in db) + 1
    return 1

# Pydantic Model

class User(BaseModel):
    id: int = Field(..., description='The auto-generated id of the user')
    name: str = Field(..., description='The name of the user')
    email: str = Field(..., description='The email of the user')
    is_active: bool = Field(..., description='The active status of the user')

# Endpoints

@app.get('/health')
async def health_check():
    return {'status': 'OK'}

@app.get('/users', response_model=List[User])
async def get_users():
    db = load_db()
    return db

@app.get('/users/{user_id}', response_model=User)
async def get_user(user_id: int):
    db = load_db()
    for user in db:
        if user['id'] == user_id:
            return user
    raise HTTPException(status_code=404, detail='User not found')

@app.post('/users', response_model=User)
async def create_user(user: User):
    db = load_db()
    user_id = get_next_id(db)
    user_dict = user.dict()
    user_dict['id'] = user_id
    db.append(user_dict)
    save_db(db)
    return user_dict

@app.put('/users/{user_id}', response_model=User)
async def update_user(user_id: int, user: User):
    db = load_db()
    for idx, existing_user in enumerate(db):
        if existing_user['id'] == user_id:
            db[idx] = user.dict()
            db[idx]['id'] = user_id
            save_db(db)
            return db[idx]
    raise HTTPException(status_code=404, detail='User not found')

@app.delete('/users/{user_id}')
async def delete_user(user_id: int):
    db = load_db()
    for idx, existing_user in enumerate(db):
        if existing_user['id'] == user_id:
            del db[idx]
            save_db(db)
            return {'message': 'User deleted'}
    raise HTTPException(status_code=404, detail='User not found')
