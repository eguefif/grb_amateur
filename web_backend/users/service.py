from typing import Annotated
from fastapi import Query, HTTPException
from sqlmodel import select

from db import SessionDep
from .models import User

def read_users(
        session: SessionDep,
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100,
            ) -> list[User]:
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users

def get_one(session: SessionDep, id: int) -> User | None:
    user = session.get(User, id)
    return user

def create(session: SessionDep, user: User) -> User:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def delete(session: SessionDep, id: int) -> bool:
    user = session.get(User, id)
    if not user:
        return False
    session.delete(user)
    session.commit()
    return True
