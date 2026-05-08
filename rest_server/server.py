from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


users_db = {
    1: {
        "id": 1,
        "name": "Antonio Marques",
        "email": "antonio@email.com",
        "phone": "+55 21 99999-9999",
        "address": "Rua Exemplo 123",
        "city": "Rio de Janeiro",
        "state": "RJ",
        "country": "Brazil",
        "zipcode": "20000-000",
        "company": "Open Systems",
        "job_title": "Software Engineer",
        "biography": "A" * 300,
        "preferences": "dark_mode=true;notifications=true;" * 5,
        "metadata": "metadata_example_" * 5,
        "notes": "important_notes_" * 5,
        "age": 28,
        "followers_count": 1247,
        "following_count": 389,
        "posts_count": 2341,
        "reputation_score": 4.7,
        "is_active": True,
        "is_verified": False,
        "is_premium": True,
        "created_at": 1714000000,
        "updated_at": 1714500000,
    },
    2: {
        "id": 2,
        "name": "Maria Silva",
        "email": "maria@email.com",
        "phone": "+55 11 98888-8888",
        "address": "Avenida Central 456",
        "city": "São Paulo",
        "state": "SP",
        "country": "Brazil",
        "zipcode": "01000-000",
        "company": "Tech Corp",
        "job_title": "Data Analyst",
        "biography": "B" * 300,
        "preferences": "light_mode=false;notifications=false;" * 5,
        "metadata": "other_metadata_" * 5,
        "notes": "secondary_notes_" * 5,
        "age": 35,
        "followers_count": 8523,
        "following_count": 142,
        "posts_count": 891,
        "reputation_score": 4.9,
        "is_active": True,
        "is_verified": True,
        "is_premium": False,
        "created_at": 1700000000,
        "updated_at": 1714600000,
    },
}


class UpdateRequest(BaseModel):
    biography: str


class UpdateResponse(BaseModel):
    success: bool


class User(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    address: str
    city: str
    state: str
    country: str
    zipcode: str
    company: str
    job_title: str
    biography: str
    preferences: str
    metadata: str
    notes: str
    age: int
    followers_count: int
    following_count: int
    posts_count: int
    reputation_score: float
    is_active: bool
    is_verified: bool
    is_premium: bool
    created_at: int
    updated_at: int


app = FastAPI()


@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    user = users_db.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.put("/users/{user_id}", response_model=UpdateResponse)
def update_user(user_id: int, req: UpdateRequest):
    if user_id in users_db:
        users_db[user_id]["biography"] = req.biography
        return UpdateResponse(success=True)
    return UpdateResponse(success=False)
