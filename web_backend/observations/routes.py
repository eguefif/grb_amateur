from typing import Annotated
import sqlalchemy
from fastapi import APIRouter, Query, HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError
from pathlib import Path
import uuid
import os

from db import SessionDep
from .models import Observation, ObservationOut
from . import service

from users.routes import CurrentActiveUserDep

router = APIRouter(prefix="/observations")

OBSERVATION_IMAGES_PATH = Path("./static/")
if not os.path.exists(OBSERVATION_IMAGES_PATH):
    raise "No static folder to create image in"


@router.post("/")
async def create_observation(
    session: SessionDep,
    observation: Observation,
    current_active_user: CurrentActiveUserDep,
) -> Observation:
    try:
        observation = service.create_observation(session, observation)
    except sqlalchemy.exc.NoResultFound:
        raise HTTPException(status_code=404, detail="Email not found")
    return observation


@router.post("/image/{observation_id}")
async def create_upload_image(
    session: SessionDep, observation_id: int, file: UploadFile
) -> str:
    try:
        image = Image.open(file.file)
    except UnidentifiedImageError:
        raise HTTPException(status_code=422, detail="Wrong format image")
    filename = f"{observation_id}-{uuid.uuid7()}"
    filename_path = f"{filename}.webp"
    output_path = OBSERVATION_IMAGES_PATH / filename_path
    image.save(output_path, "WEBP", quality=85, method=6)

    service.create_observation_file(session, f"{output_path}", observation_id)
    return file.filename


@router.get("/", response_model=list[ObservationOut])
async def read_observations(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[ObservationOut]:
    return service.read_observations(session, offset, limit)


@router.get("/alert/{id}", response_model=list[ObservationOut])
async def read_observations_from_alert_id(
    session: SessionDep,
    id: int,
) -> list[ObservationOut]:
    return service.read_observations_from_alert_id(session, id)
