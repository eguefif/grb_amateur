from typing import Annotated, Optional
from fastapi import Query, Request, Depends, Header, HTTPException
from sqlmodel import select
import json
import hmac
import hashlib
import time
import os

from db import SessionDep
from smtp_client import SMTPClient
from grb_alerts.models import GRBAlert, GRBPosition


def add_alert(session: SessionDep, alert: GRBAlert) -> GRBAlert:
    session.add(alert)
    session.commit()
    session.refresh(alert)
    return alert


def add_grb_position(session: SessionDep, grb_position: GRBPosition) -> GRBPosition:
    session.add(grb_position)
    session.commit()
    session.refresh(grb_position)
    return grb_position


def read_events(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[GRBAlert]:
    alerts = session.exec(select(GRBAlert).offset(offset).limit(limit)).all()
    return alerts


def send_notification(session: SessionDep, data):
    smtp_client = SMTPClient()

    body = "<html><body>"
    body += f"<h2>This is a {data.notice_type}</h2>"
    body += f"<p>date: {data.notice_date}</p>"
    if "position" in data.notice_type.lower():
        body += f"""
            <p>Alert comments: {data.comments}</p>
            """
    elif "alert" in data.notice_type.lower():
        body += f"""
            <p>Alert grb_ra: {data.grb_ra}</p>
            <p>Alert grb_dec: {data.grb_dec}</p>
            """
    else:
        return
    body += "<p>Emmanuel</p>"
    body += "</body></html>"
    smtp_client.send_confirmation_email(
        ["eguefif@gmail.com"], "Fermi GRB message", body
    )


async def verify_signature(
    request: Request,
    x_signature: Annotated[Optional[str], Header()] = None,
    x_timestamp: Annotated[Optional[str], Header()] = None,
):
    if not x_signature:
        raise HTTPException(status_code=401, detail="Not authorized")

    try:
        timestamp = float(x_timestamp)
        if abs(time.time() - timestamp) > 300:
            raise HTTPException(status_code=401, detail="Not authorized")
    except ValueError:
        raise HTTPException(status_code=401, detail="Not authorized")

    body = await request.body()
    event = json.loads(body)
    trigger_num = event["trigger_num"]
    message = f"{x_timestamp}:{trigger_num}".encode()
    expected_signature = hmac.new(
        os.getenv("SECRET_KEY").encode(), message, hashlib.sha256
    ).hexdigest()

    if expected_signature != x_signature:
        print("Excepected: ", expected_signature)
        print("Received: ", x_signature)
        raise HTTPException(status_code=401, detail="Not authorized")
    return True


VerifySignatureDep = Annotated[bool, Depends(verify_signature)]
