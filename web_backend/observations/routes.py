import sqlalchemy
from PIL import UnidentifiedImageError
from fastapi import APIRouter, HTTPException, UploadFile

from db import SessionDep
from .models import Observation, ObservationOut
from . import service

from users.routes import CurrentActiveUserDep

router = APIRouter(prefix="/observations")


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
    session: SessionDep,
    observation_id: int,
    file: UploadFile,
    current_active_user: CurrentActiveUserDep,
) -> str:
    try:
        service.save_image(session, observation_id, file.file)
    except UnidentifiedImageError:
        raise HTTPException(status_code=422, detail="Wrong format image")
    return file.filename


@router.get("/alert/{id}", response_model=list[ObservationOut])
async def read_observations_from_alert_id(
    session: SessionDep,
    id: int,
) -> list[ObservationOut]:
    return service.read_observations_from_alert_id(session, id)
