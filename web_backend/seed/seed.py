from faker import Faker
from db import engine
from sqlmodel import Session
from users.models import User

faker = Faker()

def generate_users(n=2):
    """Generate fake user data and return as list of dicts."""
    print(f"Generating {n} users")
    return [{'email': faker.ascii_email()} for _ in range(n)]

def create_users(n=2):
    users = []
    print(f"Creating {n} users")
    with Session(engine) as session:
        for _ in range(n):
            user = User(email= faker.ascii_email())
            session.add(user)
        session.commit()

def delete_users():
    with Session(engine) as session:
        users = session.query(User)
        if users:
            users.delete()
            session.commit()

if __name__ == "__main__":
    create_users()
