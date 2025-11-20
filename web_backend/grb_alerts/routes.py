from fastapi import APIRouter

from grb_alerts.models import GRBAlert
from grb_alerts import service
from db import SessionDep

router = APIRouter(prefix = "/events")

@router.post("/")
async def add_event(session: SessionDep, alert: GRBAlert) -> GRBAlert:
    alert = service.add_alert(session, alert)
    return alert
