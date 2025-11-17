from pydantic import BaseModel


class User(BaseModel):
    id: int
    email: str

user_fakes = [
    User(id=0, email="albert.enstein@universe.com"),
    User(id=1, email="johannes.kepler@universe.com"),
]
