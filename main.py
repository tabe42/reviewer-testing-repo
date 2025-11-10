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
    except (FileNotFoundError, json.JSONDecodeError):
        db = []
        save_db(db)
    return db

def save_db(data: List[Dict]):
    with open('users_db.json', 'w') as file:
        json.dump(data, file)

def get_next_id(db: List[Dict]) -> int:
    max_id = 0
    for user in db:
        if 'id' in user:
            max_id = max(max_id, user['id'])
    return max_id + 1

# Pydantic Models

class UserBase(BaseModel):
    name: str = Field(..., example='John Doe')
    email: str = Field(..., example='john.doe@example.com')
    is_active: bool = Field(..., example=True)

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int = Field(..., example=1)

class UserUpdate(UserBase):
    pass

# Endpoints

@app.get('/health', response_model=str)
async def health_check():
    return 'OK'

@app.get('/users/{user_id}', response_model=User, responses={404: {'description': 'User not found'}})
async def get_user(user_id: int):
    db = load_db()
    for user in db:
        if user['id'] == user_id:
            return User(**user)
    raise HTTPException(status_code=404, detail='User not found')

@app.post('/users', response_model=User, responses={400: {'description': 'Bad request'}})
async def create_user(user: UserCreate):
    db = load_db()
    user_dict = user.dict()
    user_dict['id'] = get_next_id(db)
    db.append(user_dict)
    save_db(db)
    return User(**user_dict)

@app.put('/users/{user_id}', response_model=User, responses={404: {'description': 'User not found'}, 400: {'description': 'Bad request'}})
async def update_user(user_id: int, user: UserUpdate):
    db = load_db()
    for i, existing_user in enumerate(db):
        if existing_user['id'] == user_id:
            db[i] = user.dict(exclude_unset=True)
            db[i]['id'] = user_id
            save_db(db)
            return User(**db[i])
    raise HTTPException(status_code=404, detail='User not found')

@app.delete('/users/{user_id}', responses={404: {'description': 'User not found'}})
async def delete_user(user_id: int):
    db = load_db()
    for i, existing_user in enumerate(db):
        if existing_user['id'] == user_id:
            del db[i]
            save_db(db)
            return
    raise HTTPException(status_code=404, detail='User not found')
