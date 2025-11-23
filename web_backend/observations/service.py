from typing import Annotated
from fastapi import Query

from .models import Observation, ObservationImage, ObservationOut
from users.models import User
from db import SessionDep
from sqlmodel import select


def create_observation(
    session: SessionDep, observation: Observation, email: str
) -> Observation:
    query = select(User).where(User.email == email)
    session.exec(query).one()
    session.add(observation)
    session.commit()
    session.refresh(observation)
    return observation


def read_observations(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[ObservationOut]:
    observations = session.exec(select(Observation).offset(offset).limit(limit)).all()
    observations_out = []
    for observation in observations:
        path = observation.observation_image.path
        observation_out = ObservationOut(**observation.dict(), file_path=path)
        observations_out.append(observation_out)
    return observations_out


def read_observations_from_alert_id(
    session: SessionDep, id: int
) -> list[ObservationOut]:
    query = select(Observation).where(Observation.alert_id == id)
    observations = session.exec(query).all()
    observations_out = []
    for observation in observations:
        path = observation.observation_image.path
        observation_out = ObservationOut(**observation.dict(), file_path=path)
        observations_out.append(observation_out)
    return observations_out


def get_one_observation(session: SessionDep, id: int) -> Observation:
    query = select(Observation).where(Observation.id == id)
    result = session.exec(query).one()
    return result


def create_observation_file(
    session: SessionDep, path: str, observation_id: int
) -> ObservationImage:
    observation_file = ObservationImage(path=path, observation_id=observation_id)
    session.add(observation_file)
    session.commit()
    session.refresh(observation_file)
    return observation_file
