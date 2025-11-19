import asyncio
from dotenv import load_dotenv
from sqlmodel import SQLModel
from sqlalchemy import text
from sqlalchemy import create_engine
import os

load_dotenv()

PG_USER = os.getenv("POSTGRES_USER")
PG_PASSWORD = os.getenv("POSTGRES_PASSWORD")
PG_DB = os.getenv("POSTGRES_DB")
PG_HOST = os.getenv("POSTGRES_URL")
PG_PORT = os.getenv("POSTGRES_PORT")
PG_ECHO = os.getenv("PG_ECHO") == "True"

DB_URL = f"postgresql+psycopg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"

engine = create_engine(
    DB_URL,
    echo=PG_ECHO,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True
)

def init_db():
    try:
        engine.execute(text("CREATE DATABASE grb_db"))
        print("Database created")
    except Exception:
        print("Database already exists")


if __name__ == "__main__":
    init_db()
