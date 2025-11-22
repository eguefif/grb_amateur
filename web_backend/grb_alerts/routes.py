from fastapi import APIRouter, BackgroundTasks

from grb_alerts.models import GRBAlert, GRBPosition
from grb_alerts import service
from db import SessionDep
from smtp_client import SMTPClient

router = APIRouter(prefix="/events")


def send_notification(session: SessionDep, data):
    smtp_client = SMTPClient()

    body = "<html><body>"
    body += f"<h2>This is a {data.notice_type}</h2>"
    body += f"<p>date: {data.notice_date}</p>"
    if 'position' in data.notice_type.lower():
        body += f"""
            <p>Alert comments: {data.comments}</p>
            """
    elif 'alert' in data.notice_type.lower():
        body += f"""
            <p>Alert grb_ra: {data.grb_ra}</p>
            <p>Alert grb_dec: {data.grb_dec}</p>
            """
    else:
        return
    body += "<p>Emmanuel</p>"
    body += "</body></html>"
    smtp_client.send_confirmation_email(['eguefif@gmail.com'], "Fermi GRB message", body)

@router.post("/")
async def add_event(
        session: SessionDep,
        alert: GRBAlert,
        background_tasks: BackgroundTasks
    ) -> GRBAlert:
    alert = service.add_alert(session, alert)
    background_tasks.add_task(send_notification, session, alert)
    return alert

@router.post("/position")
async def add_event(
        session: SessionDep,
        grb_position: GRBPosition,
        background_tasks: BackgroundTasks
    ) -> GRBPosition:
    grb_position = service.add_grb_position(session, grb_position)
    background_tasks.add_task(send_notification, session, grb_position)
    return grb_position

@router.get("/last_events")
async def last_events(session: SessionDep) -> list[GRBAlert]:
    alerts = service.read_events(session, offset=0, limit=5)
    if not alerts:
        raise HTTPException(status_code=404, detail="No events yet")
    return alerts
