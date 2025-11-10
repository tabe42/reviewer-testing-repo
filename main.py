import json
from typing import List, Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()


class User(BaseModel):
    id: int = Field(..., description="The unique ID of the user")
    name: str = Field(..., description="The name of the user")
    email: str = Field(..., description="The email of the user")
    is_active: bool = Field(..., description="The active status of the user")


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
    if not db:
        return 1
    return max(user['id'] for user in db) + 1


@app.get('/health')
def health_check():
    return {'status': 'OK'}


@app.post('/users/', response_model=User)
def create_user(user: User):
    db = load_db()
    user_dict = user.dict()
    user_dict['id'] = get_next_id(db)
    db.append(user_dict)
    save_db(db)
    return user


@app.get('/users/{user_id}', response_model=User)
def read_user(user_id: int):
    db = load_db()
    user = next((user for user in db if user['id'] == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.put('/users/{user_id}', response_model=User)
def update_user(user_id: int, user: User):
    db = load_db()
    for index, existing_user in enumerate(db):
        if existing_user['id'] == user_id:
            db[index] = user.dict()
            db[index]['id'] = user_id
            save_db(db)
            return db[index]
    raise HTTPException(status_code=404, detail="User not found")


@app.delete('/users/{user_id}')
def delete_user(user_id: int):
    db = load_db()
    for index, existing_user in enumerate(db):
        if existing_user['id'] == user_id:
            del db[index]
            save_db(db)
            return {'message': 'User deleted'}
    raise HTTPException(status_code=404, detail="User not found")