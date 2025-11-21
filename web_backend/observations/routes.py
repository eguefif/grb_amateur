from fastapi import APIRouter
from db import SessionDep
from .models import Observation
from . import service

router = APIRouter(prefix = "/observations")

@router.post("/")
async def create_observation(session: SessionDep, observation: Observation) -> Observation:
    return service.create_observation(session, observation)
