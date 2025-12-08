import os
from fastapi import HTTPException
from sqlmodel import select

from db import SessionDep
from .models import User, UserIn
from smtp_client import SMTPClient

from pwdlib import PasswordHash


def get_one_by_email(session: SessionDep, email: str) -> User | None:
    query = select(User).where(User.email == email)
    user = session.exec(query).one()
    return user


def send_confirmation_email(email: str):
    smtp_client = SMTPClient()
    backend_domain = os.getenv("DOMAIN")

    body = "<html><body>"
    body += "<h2>Hello</h2>"
    body += "<p>Please confirm your email address by going to the following addres</p>"
    body += (
        f'<p><a href="{backend_domain}/api/users/confirm/{email}">Confirmation link</a></p>'
    )
    body += "<p>Emmanuel</p>"
    body += "</body></html>"
    smtp_client.send_email([email], "Email Confirmation", body)


def get_password_hash(password: str) -> str:
    password_hash = PasswordHash.recommended()
    return password_hash.hash(password)


def create(session: SessionDep, user: UserIn) -> User:
    if user.password != user.password_confirmation:
        raise HTTPException(status_code=400, detail="Password does not match")

    hashed_password = get_password_hash(user.password)
    user_dict = user.dict()
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
