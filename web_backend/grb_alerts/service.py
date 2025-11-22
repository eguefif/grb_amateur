from typing import Annotated
from fastapi import Query
from sqlmodel import select

from db import SessionDep

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
