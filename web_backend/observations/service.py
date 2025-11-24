from typing import Annotated
from PIL import Image
from pathlib import Path
import uuid
import os

from fastapi import Query, File

from .models import Observation, ObservationImage, ObservationOut
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


def create_observation_file(
    session: SessionDep, path: str, observation_id: int
) -> ObservationImage:
    observation_file = ObservationImage(path=path, observation_id=observation_id)
    session.add(observation_file)
    session.commit()
    session.refresh(observation_file)
    return observation_file


def save_image(session: SessionDep, observation_id: int, file: File):
    OBSERVATION_IMAGES_PATH = Path("./static/")
    if not os.path.exists(OBSERVATION_IMAGES_PATH):
        raise "No static folder to create image in"

    image = Image.open(file)
    filename = f"{observation_id}-{uuid.uuid7()}"
    filename_path = f"{filename}.webp"
    output_path = OBSERVATION_IMAGES_PATH / filename_path
    image.save(output_path, "WEBP", quality=85, method=6)

    create_observation_file(session, f"{output_path}", observation_id)
