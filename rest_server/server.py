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
        "biography": "A" * 5000,
        "preferences": "dark_mode=true;notifications=true;" * 100,
        "metadata": "metadata_example_" * 200,
        "notes": "important_notes_" * 300,
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
        "biography": "B" * 5000,
        "preferences": "light_mode=false;notifications=false;" * 100,
        "metadata": "other_metadata_" * 200,
        "notes": "secondary_notes_" * 300,
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
