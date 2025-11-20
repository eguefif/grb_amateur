from db import SessionDep

from grb_alerts.models import GRBAlert


def add_alert(session: SessionDep, alert: GRBAlert) -> GRBAlert:
    session.add(alert)
    session.commit()
    session.refresh(alert)
    return alert
