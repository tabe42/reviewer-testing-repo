import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

# Helper functions
def load_db() -> list:
    try:
        with open('users_db.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_db(data: list):
    with open('users_db.json', 'w') as file:
        json.dump(data, file, indent=4)

def get_next_id(db: list) -> int:
    if db:
        return max(user['id'] for user in db) + 1
    else:
        return 1

# Pydantic model for user
class User(BaseModel):
    id: int = Field(..., example=1)
    name: str = Field(..., example='John Doe')
    email: str = Field(..., example='john.doe@example.com')
    is_active: bool = Field(..., example=True)

# Endpoints
@app.get('/health')
def health_check():
    return {'status': 'OK'}

@app.post('/users', response_model=User)
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
            db[idx] = user.dict()
            save_db(db)
            return user
    raise HTTPException(status_code=404, detail='User not found')

@app.delete('/users/{user_id}')
def delete_user(user_id: int):
    db = load_db()
    for idx, existing_user in enumerate(db):
        if existing_user['id'] == user_id:
            del db[idx]
            save_db(db)
            return
    raise HTTPException(status_code=404, detail='User not found')
