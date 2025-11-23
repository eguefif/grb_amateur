from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import users.routes
import grb_alerts.routes
import observations.routes

load_dotenv()

app = FastAPI()

app.include_router(users.routes.router)
app.include_router(grb_alerts.routes.router)
app.include_router(observations.routes.router)

app.mount("/static", StaticFiles(directory="static"), name="static")
