from sqlalchemy.exc import IntegrityError
from typing import Annotated

from fastapi import APIRouter, Query, HTTPException

import users.service as service
from users.models import User

from db import SessionDep

router = APIRouter(prefix="/users")


@router.get("/")
async def root(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[User]:
    return service.read_users(session, offset, limit)


@router.get("/{id}")
async def get_one(session: SessionDep, id: int) -> User | None:
    user = service.get_one(session, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/")
async def create_user(session: SessionDep, user: User) -> User:
    try:
        service.create(session, user)
    except IntegrityError:
        raise HTTPException(status_code=403, detail="Email already exists")
    return service.create(session, user)


@router.delete("/")
async def delete_user(session: SessionDep, user_id: int) -> bool | None:
    if service.delete(session, user_id):
        return True
    return False
