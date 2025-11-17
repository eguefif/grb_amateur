from .models import user_fakes as data, User

def get_all() -> list[User]:
    return data

def get_one(id: int) -> User | None:
    for user in data:
        if user.id == id:
            return user
    return None

def create(user: User) -> User:
    data.append(user)
    return user

def modify(id: int, user: User) -> User:
    return user

def replace(id: int, user: User) -> User:
    return user

def delete(id: int) -> bool:
    return None
