from typing import List, Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import json

app = FastAPI()

# Data storage file
DB_FILE = 'users_db.json'

# Pydantic models
class User(BaseModel):
    id: int = Field(..., description="The auto-generated id of the user")
    name: str = Field(..., description="The name of the user")
    email: str = Field(..., description="The email of the user")
    is_active: bool = Field(..., description="The active status of the user")

class UserCreate(BaseModel):
    name: str = Field(..., description="The name of the user")
    email: str = Field(..., description="The email of the user")
    is_active: bool = Field(..., description="The active status of the user")

# Helper functions
def load_db() -> List[Dict]:
    try:
        with open(DB_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        with open(DB_FILE, 'w') as file:
            json.dump([], file)
        return []

def save_db(data: List[Dict]):
    with open(DB_FILE, 'w') as file:
        json.dump(data, file)

def get_next_id(db: List[Dict]) -> int:
    return max((user['id'] for user in db), default=0) + 1

# Endpoints
@app.get("/healthcheck", response_model=dict, status_code=200)
def healthcheck():
    return {"status": "ok"}

@app.get("/users/{user_id}", response_model=User, status_code=200)
def get_user(user_id: int):
    db = load_db()
    for user in db:
        if user['id'] == user_id:
            return User(**user)
    raise HTTPException(status_code=404, detail="User not found")

@app.post("/users", response_model=User, status_code=201)
def create_user(user: UserCreate):
    db = load_db()
    next_id = get_next_id(db)
    new_user = user.dict()
    new_user['id'] = next_id
    db.append(new_user)
    save_db(db)
    return User(**new_user)

@app.put("/users/{user_id}", response_model=User, status_code=200)
def update_user(user_id: int, user: UserCreate):
    db = load_db()
    for i, existing_user in enumerate(db):
        if existing_user['id'] == user_id:
            db[i] = user.dict()
            db[i]['id'] = user_id
            save_db(db)
            return User(**db[i])
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int):
    db = load_db()
    for i, existing_user in enumerate(db):
        if existing_user['id'] == user_id:
            del db[i]
            save_db(db)
            return
    raise HTTPException(status_code=404, detail="User not found")
