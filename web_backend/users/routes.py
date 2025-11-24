import os
from typing import Annotated
from sqlalchemy.exc import IntegrityError, NoResultFound

from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm

import users.service as service
from users.models import UserOut, UserIn, Token
from .auth import authenticate_user, create_access_token, CurrentActiveUserDep

from db import SessionDep


router = APIRouter(prefix="/users")


@router.post("/token")
async def login(
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    Main entry point for authentication. A user that authenticate in sing-in will send
    a request to this endpoint.

    Note that username = email

    We have to use username because of OAuth2PasswrodRequestForm.
    """
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Your accound is deactivated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.email})
    return Token(access_token=access_token, token_type="Bearer")


@router.get("/me")
async def get_users_me(current_user: CurrentActiveUserDep) -> UserOut:
    return current_user


@router.post("/")
async def create_user(
    session: SessionDep, user: UserIn, background_tasks: BackgroundTasks
) -> UserOut:
    try:
        user = service.create(session, user)
    except IntegrityError:
        raise HTTPException(status_code=403, detail="Email already exists")

    background_tasks.add_task(service.send_confirmation_email, user.email)
    return UserOut(**user.dict())


@router.get("/confirm/{email}", response_class=RedirectResponse)
def confirm_email(session: SessionDep, email: str) -> str:
    try:
        service.confirm_email(session, email)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Email not found")
    if os.getenv("DEV") == "True":
        return RedirectResponse("http://localhost:5173/email-confirmed")
    else:
        domain = os.getenv("DOMAIN")
        return RedirectResponse(f"{domain}/email-confirmed")
