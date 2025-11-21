from typing import Annotated
from fastapi import Query

from .models import Observation
from db import SessionDep
from sqlmodel import select


def create_observation(session: SessionDep, observation: Observation) -> Observation:
    session.add(observation)
    session.commit()
    session.refresh(observation)
    return observation


def read_observations(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Observation]:
    return session.exec(select(Observation).offset(offset).limit(limit)).all()
