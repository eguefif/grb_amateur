import os
from typing import Annotated
from fastapi import Query, HTTPException
from sqlmodel import select

from db import SessionDep
from .models import User, UserIn
from smtp_client import SMTPClient

from pwdlib import PasswordHash


def read_users(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[User]:
    query = select(User).where(User.email_confirmed).offset(offset).limit(limit)
    users = session.exec(query).all()
    return users


def get_one(session: SessionDep, id: int) -> User | None:
    user = session.get(User, id)
    return user


def get_one_by_email(session: SessionDep, email: str) -> User | None:
    query = select(User).where(User.email == email)
    user = session.exec(query).one()
    return user


def send_confirmation_email(email: str):
    smtp_client = SMTPClient()
    backend_domain = os.getenv("BACKEND_DOMAIN")

    body = "<html><body>"
    body += "<h2>Hello</h2>"
    body += "<p>Please confirm your email address by going to the following addres</p>"
    body += (
        f'<p><a href="{backend_domain}/users/confirm/{email}">Confirmation link</a></p>'
    )
    body += "<p>Emmanuel</p>"
    body += "</body></html>"
    smtp_client.send_confirmation_email([email], "Email Confirmation", body)


def get_password_hash(password: str) -> str:
    password_hash = PasswordHash.recommended()
    return password_hash.hash(password)


def create(session: SessionDep, user: UserIn) -> User:
    if user.password != user.password_confirmation:
        raise HTTPException(status_code=400, detail="Password does not match")
    hashed_password = get_password_hash(user.password)
    user_dict = user.dict()
    user_dict.pop("password")
    user_dict.pop("password_confirmation")
    new_user = User(**user_dict, hashed_password=hashed_password)
    new_user.email_confirmed = False
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


def confirm_email(session: SessionDep, email: str) -> True:
    query = select(User).where(User.email == email)
    user = session.exec(query).one()
    user.email_confirmed = True
    session.add(user)
    session.commit()
    return True


def delete(session: SessionDep, id: int) -> bool:
    user = session.get(User, id)
    if not user:
        return False
    session.delete(user)
    session.commit()
    return True
