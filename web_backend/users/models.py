from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    email: str = Field(index=True, unique=True)
    full_name: str
    email_confirmed: bool | None = False


class User(UserBase, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str


class UserIn(UserBase):
    password: str
    password_confirmation: str


class UserOut(UserBase):
    id: int
