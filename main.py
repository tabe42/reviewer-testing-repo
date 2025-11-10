from typing import List, Dict
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Helper functions
def load_db() -> List[Dict]:
    try:
        with open('users_db.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        with open('users_db.json', 'w') as file:
            json.dump([], file)
        return []

def save_db(data: List[Dict]) -> None:
    with open('users_db.json', 'w') as file:
        json.dump(data, file)

def get_next_id(db: List[Dict]) -> int:
    return max((user['id'] for user in db), default=0) + 1

# Pydantic model for user
class User(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool

# Health check endpoint
@app.get('/health')
def health_check():
    return {'status': 'ok'}

# Create a user
@app.post('/users', response_model=User)
def create_user(user: User):
    db = load_db()
    user.id = get_next_id(db)
    db.append(user.dict())
    save_db(db)
    return user

# Get a user by ID
@app.get('/users/{user_id}', response_model=User)
def get_user(user_id: int):
    db = load_db()
    for user in db:
        if user['id'] == user_id:
            return User(**user)
    raise HTTPException(status_code=404, detail='User not found')

# Update a user
@app.put('/users/{user_id}', response_model=User)
def update_user(user_id: int, user: User):
    db = load_db()
    for i, existing_user in enumerate(db):
        if existing_user['id'] == user_id:
            db[i] = user.dict()
            save_db(db)
            return user
    raise HTTPException(status_code=404, detail='User not found')

# Delete a user
@app.delete('/users/{user_id}')
def delete_user(user_id: int):
    db = load_db()
    for i, existing_user in enumerate(db):
        if existing_user['id'] == user_id:
            del db[i]
            save_db(db)
            return
    raise HTTPException(status_code=404, detail='User not found')
