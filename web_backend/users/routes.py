from sqlalchemy.exc import IntegrityError, NoResultFound
from typing import Annotated

from fastapi import APIRouter, Query, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse

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
async def create_user(
    session: SessionDep, user: User, background_tasks: BackgroundTasks
) -> User:
    try:
        service.create(session, user)
    except IntegrityError:
        raise HTTPException(status_code=403, detail="Email already exists")

    background_tasks.add_task(service.send_confirmation_email, user.email)
    return service.create(session, user)


@router.get("/confirm/{email}", response_class=HTMLResponse)
def confirm_email(session: SessionDep, email: str) -> str:
    try:
        service.confirm_email(session, email)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Email not found")
    return """
                <html><body>
                <p>Email confirmed</p>
                </body></html>
            """


@router.delete("/")
async def delete_user(session: SessionDep, user_id: int) -> bool | None:
    if service.delete(session, user_id):
        return True
    return False
