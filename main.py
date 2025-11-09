from typing import List, Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import json

app = FastAPI()

# Helper functions

def load_db() -> List[Dict]:
    try:
        with open('users_db.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        with open('users_db.json', 'w') as f:
            json.dump([], f)
        return []

def save_db(data: List[Dict]):
    with open('users_db.json', 'w') as f:
        json.dump(data, f)

def get_next_id(db: List[Dict]) -> int:
    if db:
        return max(user['id'] for user in db) + 1
    else:
        return 1

# Pydantic models

class UserBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    email: str = Field(..., min_length=1, max_length=50)
    is_active: bool = Field(..., alias='active')

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

# Endpoints

@app.get("/health")
def health_check():
    return {'status': 'OK'}


@app.get("/users/", response_model=List[User])
def get_users():
    db = load_db()
    return db


@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    db = load_db()
    for user in db:
        if user['id'] == user_id:
            return User(**user)
    raise HTTPException(status_code=404, detail="User not found")


@app.post("/users/", response_model=User)
def create_user(user: UserCreate):
    db = load_db()
    new_id = get_next_id(db)
    new_user = user.dict()
    new_user['id'] = new_id
    db.append(new_user)
    save_db(db)
    return User(**new_user)


@app.put("/users/{user_id}/", response_model=User)
def update_user(user_id: int, user: UserCreate):
    db = load_db()
    for i, u in enumerate(db):
        if u['id'] == user_id:
            db[i] = user.dict()
            db[i]['id'] = user_id
            save_db(db)
            return User(**db[i])
    raise HTTPException(status_code=404, detail="User not found")


@app.delete("/users/{user_id}/", response_model=User)
def delete_user(user_id: int):
    db = load_db()
    for i, user in enumerate(db):
        if user['id'] == user_id:
            removed_user = db.pop(i)
            save_db(db)
            return User(**removed_user)
    raise HTTPException(status_code=404, detail="User not found")
