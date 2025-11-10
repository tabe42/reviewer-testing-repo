from typing import List, Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import json

app = FastAPI()

# Helper Functions

def load_db() -> List[Dict]:
    try:
        with open('users_db.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        with open('users_db.json', 'w') as file:
            json.dump([], file)
        return []

def save_db(data: List[Dict]):
    with open('users_db.json', 'w') as file:
        json.dump(data, file)

def get_next_id(db: List[Dict]) -> int:
    if not db:
        return 1
    return max(user['id'] for user in db) + 1


# Pydantic Model

class User(BaseModel):
    id: int = Field(..., example=1)
    name: str = Field(..., example='John Doe')
    email: str = Field(..., example='john@example.com')
    is_active: bool = Field(..., example=True)


# Endpoints

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
    user_id = get_next_id(db)
    user_dict = user.dict()
    user_dict['id'] = user_id
    db.append(user_dict)
    save_db(db)
    return user_dict


@app.put('/users/{user_id}', response_model=User)
def update_user(user_id: int, user: User):
    db = load_db()
    for i, existing_user in enumerate(db):
        if existing_user['id'] == user_id:
            db[i] = user.dict()
            db[i]['id'] = user_id
            save_db(db)
            return db[i]
    raise HTTPException(status_code=404, detail='User not found')


@app.delete('/users/{user_id}')
def delete_user(user_id: int):
    db = load_db()
    for i, existing_user in enumerate(db):
        if existing_user['id'] == user_id:
            del db[i]
            save_db(db)
            return {'message': 'User deleted'}
    raise HTTPException(status_code=404, detail='User not found')
