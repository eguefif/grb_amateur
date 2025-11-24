from datetime import timedelta, timezone, datetime
from typing import Annotated

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from pwdlib import PasswordHash
import jwt
from jwt import InvalidTokenError

import os

import users.service as service
from users.models import UserOut, User
from db import SessionDep


SECRET_KEY = os.getenv("PASSWORD_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")
password_hash = PasswordHash.recommended()


def verify_password(plain_password: str, hashed_password: str) -> str:
    return password_hash.verify(plain_password, hashed_password)


def authenticate_user(session: SessionDep, email: str, password: str) -> User | bool:
    user = service.get_one_by_email(session, email)
    if not user:
        return False
    if not user.email_confirmed:
        raise HTTPException(status_code=404, detail="Your account is not activated")
    if not verify_password(password, user.hashed_password):
        return False
    return user


def get_current_user(
    session: SessionDep, token: Annotated[str, Depends(oauth2_scheme)]
) -> UserOut:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid Authentication Detail",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = payload.get("sub")
        if user_email is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = service.get_one_by_email(session, user_email)
    if user is None:
        raise credentials_exception
    return user

    return UserOut(**user.dict())


CurrentUserDep = Annotated[UserOut, Depends(get_current_user)]


def get_current_active_user(current_user: CurrentUserDep) -> UserOut:
    if not current_user.email_confirmed:
        raise HTTPException(status_code=400, detail="You account is deactivated")
    return current_user


CurrentActiveUserDep = Annotated[UserOut, Depends(get_current_active_user)]


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
