from typing import List, Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import json

app = FastAPI()


def load_db() -> List[Dict]:
    try:
        with open('users_db.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        with open('users_db.json', 'w') as file:
            json.dump([], file)
        return []


def save_db(data: List[Dict]):
    with open('users_db.json', 'w') as file:
        json.dump(data, file)


def get_next_id(db: List[Dict]) -> int:
    return max((user['id'] for user in db), default=0) + 1


class User(BaseModel):
    id: int = Field(..., alias='id')
    name: str = Field(..., alias='name')
    email: str = Field(..., alias='email')
    is_active: bool = Field(..., alias='is_active')


@app.get('/health')
def health_check():
    return {'status': 'OK'}


@app.get('/users/', response_model=List[User])
def get_users():
    db = load_db()
    return db


@app.get('/users/{user_id}', response_model=User)
def get_user(user_id: int):
    db = load_db()
    user = next((user for user in db if user['id'] == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user


@app.post('/users/', response_model=User)
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
    user_dict = user.dict()
    user_dict['id'] = user_id
    for i, existing_user in enumerate(db):
        if existing_user['id'] == user_id:
            db[i] = user_dict
            save_db(db)
            return user_dict
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
