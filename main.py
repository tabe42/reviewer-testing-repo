from typing import List, Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import json

app = FastAPI()


def load_db() -> List[Dict]:
    try:
        with open('users_db.json', 'r') as file:
            data = json.load(file)
        if not data:
            raise ValueError
    except (FileNotFoundError, ValueError):
        with open('users_db.json', 'w') as file:
            json.dump([], file)
        return []
    return data


def save_db(data: List[Dict]):
    with open('users_db.json', 'w') as file:
        json.dump(data, file)


def get_next_id(db: List[Dict]) -> int:
    max_id = 0
    for user in db:
        if 'id' in user and user['id'] > max_id:
            max_id = user['id']
    return max_id + 1 if max_id > 0 else 1


class User(BaseModel):
    id: int = Field(..., example=1)
    name: str = Field(..., example='John Doe')
    email: str = Field(..., example='john.doe@example.com')
    is_active: bool = Field(..., example=True)


@app.get('/health')
def health_check():
    return {'status': 'OK'}


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
    return user


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
    for idx, user in enumerate(db):
        if user['id'] == user_id:
            del db[idx]
            save_db(db)
            return {'message': 'User deleted'}
    raise HTTPException(status_code=404, detail='User not found')