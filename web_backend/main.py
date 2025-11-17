from dotenv import load_dotenv

from fastapi import FastAPI

import users.routes

load_dotenv()

app = FastAPI()

app.include_router(users.routes.router)
