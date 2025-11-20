from sqlmodel import SQLModel, Field, Relationship
from grb_alerts.models import GRBAlert


class Observation(SQLModel, table=True):
    __tablename__ = 'observations'

    id: int | None = Field(default=None, primary_key=True)
    coordinates: str
    celestial_reference: str
    equinox: str
    epoch: str
    wave_length: str
    instrument: str
    magnitude: str
    observed_time: str

    alert_id: int = Field(default=None, foreign_key="grb_alerts.id")
    alert: GRBAlert = Relationship(back_populates="grb_alerts")
