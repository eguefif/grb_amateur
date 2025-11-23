from datetime import timedelta, timezone, datetime
from sqlalchemy.exc import IntegrityError, NoResultFound
from typing import Annotated
from pydantic import BaseModel

from fastapi import APIRouter, Query, HTTPException, BackgroundTasks, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse

from pwdlib import PasswordHash
import jwt

import os

import users.service as service
from users.models import User, UserOut, UserIn

from db import SessionDep

SECRET_KEY = os.getenv("PASSWORD_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

router = APIRouter(prefix="/users")

## Auth Logic

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")
password_hash = PasswordHash.recommended()

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_email: str | None = None

def verify_password(plain_password: str, hashed_password: str) -> str:
    return password_hash.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return password_hash.hash(password)

def authenticate_user(session: SessionDep, email: str, password: str) -> user | bool:
    user = service.get_one_by_email(session, email)
    if not user:
        return False
    print("hashed: ", get_password_hash(password))
    if not verify_password(password, user.hashed_password):
        return False
    return user
    

def get_current_user(
        session: SessionDep, 
        token: Annotated[str, Depends(oauth2_scheme)]
) -> UserOut:
    credentials_exception = HTTPException(
            status_code=401,
            detail="Invalid Authentication Detail",
            headers={"WWW-Authenticate": "Bearer"}
            )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = payload.get("sub")
        if user_email is None:
            raise credentials_exception
        token_data = TokenData(user_email=user_email)
    except InvalidTokenError:
        raise credentials_exception
    user = service.get_one_by_email(session, user_email)
    if user is None:
        raise credentials_exception
    return user

    return UserOut(**user.dict())

CurrentUser = Annotated[UserOut, Depends(get_current_user)]

def get_current_active_user(current_user: CurrentUser) -> UserOut:
    if not current_user.email_confirmed:
        raise HTTPException(
            status_code=400, detail="You account is deactivated"
        )
    return current_user

CurrentActiveUser = Annotated[UserOut, Depends(get_current_active_user)]

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else: 
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({'exp': expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/token")
async def login(
        session: SessionDep,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401, 
            detail="Your accound is deactivated",
            headers={"WWW-Authenticate": "Bearer"}
            )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
                data={'sub': user.email}, expires_delta=access_token_expires
        )
    return Token(access_token=access_token, token_type="Bearer")

@router.get("/me")
async def get_users_me(current_user: CurrentActiveUser) -> UserOut:
    return current_user


### Email Creation

@router.post("/")
async def create_user(
    session: SessionDep, user: UserIn, background_tasks: BackgroundTasks
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
