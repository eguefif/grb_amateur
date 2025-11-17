from fastapi import APIRouter

import users.service
from users.models import User

router = APIRouter(prefix = "/users")

@router.get("/")
async def root() -> list[User]:
    return service.get_all()

@router.get("/{id}")
async def get_one(id) -> User | None:
    return service.get_one(id)

@router.post("/")
async def create_user(user: User) -> User:
    return service.create(user)

@router.patch("/")
async def modify_user(user: User) -> User:
    return service.modify(user)

@router.put("/")
async def replace_user(user: User) -> User:
    return service.replace(user)

@router.delete("/")
async def delete_user(user_id: int) -> bool | None:
    return service.delete(user_id)
