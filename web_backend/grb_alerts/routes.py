from fastapi import APIRouter

from grb_alerts.models import GRBAlert, GRBPosition
from grb_alerts import service
from db import SessionDep

router = APIRouter(prefix="/events")


@router.post("/")
async def add_event(session: SessionDep, alert: GRBAlert) -> GRBAlert:
    alert = service.add_alert(session, alert)
    return alert

@router.post("/position")
async def add_event(session: SessionDep, grb_position: GRBPosition) -> GRBPosition:
    grb_position = service.add_grb_position(session, grb_position)
    return grb_position



@router.get("/last_events")
async def last_events(session: SessionDep) -> list[GRBAlert]:
    alerts = service.read_events(session, offset=0, limit=5)
    if not alerts:
        raise HTTPException(status_code=404, detail="No events yet")
    return alerts
