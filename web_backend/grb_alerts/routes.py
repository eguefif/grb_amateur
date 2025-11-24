from fastapi import APIRouter, BackgroundTasks, HTTPException

from grb_alerts.models import GRBAlert, GRBPosition
from grb_alerts import service
from db import SessionDep

router = APIRouter(prefix="/events")


@router.post("/alert")
async def add_event(
    session: SessionDep,
    alert: GRBAlert,
    background_tasks: BackgroundTasks,
    verified: service.VerifySignatureDep,
) -> GRBAlert:
    alert = service.add_alert(session, alert)
    background_tasks.add_task(service.send_notification, session, alert)
    return alert


@router.post("/position")
async def add_position(
    session: SessionDep,
    grb_position: GRBPosition,
    background_tasks: BackgroundTasks,
    verified: service.VerifySignatureDep,
) -> GRBPosition:
    grb_position = service.add_grb_position(session, grb_position)
    background_tasks.add_task(service.send_notification, session, grb_position)
    return grb_position


@router.get("/last_events")
async def last_events(session: SessionDep) -> list[GRBAlert]:
    alerts = service.read_events(session, offset=0, limit=5)
    if not alerts:
        raise HTTPException(status_code=404, detail="No events yet")
    return alerts
