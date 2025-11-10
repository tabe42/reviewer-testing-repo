from typing import List, Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import json

app = FastAPI()

# Helper functions

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
    if db:
        return max(user['id'] for user in db) + 1
    return 1


# Pydantic model for User

class User(BaseModel):
    id: int = Field(..., description='The unique id of the user')
    name: str = Field(..., description='The name of the user')
    email: str = Field(..., description='The email of the user')
    is_active: bool = Field(..., description='The active status of the user')


# Endpoints

@app.get('/health')
async def health_check():
    return {'status': 'OK'}


@app.get('/users/{user_id}', response_model=User)
async def get_user(user_id: int):
    db = load_db()
    user = next((user for user in db if user['id'] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user


@app.post('/users', response_model=User)
async def create_user(user: User):
    db = load_db()
    user_dict = user.dict()
    user_dict['id'] = get_next_id(db)
    db.append(user_dict)
    save_db(db)
    return user_dict


@app.put('/users/{user_id}', response_model=User)
async def update_user(user_id: int, user: User):
    db = load_db()
    user_index = next((index for index, u in enumerate(db) if u['id'] == user_id), None)
    if not user_index:
        raise HTTPException(status_code=404, detail='User not found')
    db[user_index] = user.dict()
    save_db(db)
    return db[user_index]


@app.delete('/users/{user_id}', response_model=User)
async def delete_user(user_id: int):
    db = load_db()
    user_index = next((index for index, u in enumerate(db) if u['id'] == user_id), None)
    if not user_index:
        raise HTTPException(status_code=404, detail='User not found')
    removed_user = db.pop(user_index)
    save_db(db)
    return removed_user
