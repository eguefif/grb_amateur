from typing import Annotated
import sqlalchemy
from fastapi import APIRouter, Query, HTTPException, UploadFile
from PIL import Image
from pathlib import Path
import uuid

from db import SessionDep
from .models import Observation
from . import service

router = APIRouter(prefix="/observations")

OBSERVATION_IMAGES_PATH = Path("./observation_images/")


@router.post("/{email}")
async def create_observation(
    session: SessionDep, observation: Observation, email: str
) -> Observation:
    try:
        observation = service.create_observation(session, observation, email)
    except sqlalchemy.exc.NoResultFound:
        raise HTTPException(status_code=404, detail="Email not found")
    return observation


@router.post("/image/{observation_id}")
async def create_upload_image(
    session: SessionDep, observation_id: int, file: UploadFile
) -> str:
    image = Image.open(file.file)
    filename = f"{observation_id}-{uuid.uuid7()}"
    filename_path = f"{Path(filename)}.webp"
    output_path = OBSERVATION_IMAGES_PATH / filename_path
    image.save(output_path, "WEBP", quality=85, method=6)

    service.create_observation_file(session, f"{output_path}", observation_id)
    return file.filename


@router.get("/")
async def read_observations(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Observation]:
    return service.read_observations(session, offset, limit)


@router.get("/alert/{id}")
async def read_observations_from_alert_id(
    session: SessionDep,
    id: int,
) -> list[Observation]:
    return service.read_observations_from_alert_id(session, id)
