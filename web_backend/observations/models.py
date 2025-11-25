from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from grb_alerts.models import GRBAlert


class CoordinateSystem(str, Enum):
    icrs_j2000 = "icrs_j2000"
    fk5_j2000 = "fk5_j2000"
    b1950 = "b1950"
    galactic = "galactic"
    current_equinox = "current_equinox"


class ObservationBase(SQLModel):
    coordinates: str
    coordinate_system: CoordinateSystem = CoordinateSystem.icrs_j2000
    instrument: str
    observed_time: str


class Observation(ObservationBase, table=True):
    __tablename__ = "observations"
    id: int | None = Field(default=None, primary_key=True)

    alert_id: int = Field(default=None, foreign_key="grb_alerts.id")
    alert: GRBAlert = Relationship(back_populates="observations")

    observation_image: "ObservationImage" = Relationship(back_populates="observation")


class ObservationOut(ObservationBase):
    id: int
    file_path: str


class ObservationImage(SQLModel, table=True):
    __tablename__ = "observation_images"

    id: int | None = Field(default=None, primary_key=True)
    path: str

    observation_id: int = Field(default=None, foreign_key="observations.id")
    observation: Observation = Relationship(back_populates="observation_image")
