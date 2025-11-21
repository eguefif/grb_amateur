from typing import Annotated
from fastapi import APIRouter, Query
from db import SessionDep
from .models import Observation
from . import service

router = APIRouter(prefix="/observations")


@router.post("/")
async def create_observation(
    session: SessionDep, observation: Observation
) -> Observation:
    return service.create_observation(session, observation)


@router.get("/")
async def read_observations(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Observation]:
    return service.read_observations(session, offset, limit)
