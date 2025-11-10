from fastapi import FastAPI, HTTPException
from typing import List, Dict
import json

app = FastAPI()


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
    if db:
        return max(user['id'] for user in db) + 1
    return 1


from pydantic import BaseModel, Field


class User(BaseModel):
    id: int = Field(..., description='The auto-generated id of the user')
    name: str = Field(..., description='The name of the user')
    email: str = Field(..., description='The email of the user')
    is_active: bool = Field(..., description='The active status of the user')


@app.get('/health')
def health_check():
    return {'status': 'OK'}


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
    for idx, existing_user in enumerate(db):
        if existing_user['id'] == user_id:
            user_dict = user.dict()
            user_dict['id'] = existing_user['id']
            db[idx] = user_dict
            save_db(db)
            return User(**user_dict)
    raise HTTPException(status_code=404, detail='User not found')


@app.delete('/users/{user_id}', response_model=User)
def delete_user(user_id: int):
    db = load_db()
    for idx, existing_user in enumerate(db):
        if existing_user['id'] == user_id:
            del db[idx]
            save_db(db)
            return User(**existing_user)
    raise HTTPException(status_code=404, detail='User not found')
