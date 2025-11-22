from sqlmodel import SQLModel, Field, Relationship
from grb_alerts.models import GRBAlert, GRBPosition


class Observation(SQLModel, table=True):
    __tablename__ = "observations"

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
    alert: GRBAlert = Relationship(back_populates="observations")

    grb_position_id: int | None = Field(default=None, foreign_key="grb_positions.id")
    grb_position: GRBPosition | None = Relationship(back_populates="observations")
