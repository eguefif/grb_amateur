from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from observations.models import Observation

class GRBAlert(SQLModel, table=True):
    __tablename__ = 'grb_alerts'

    id: int | None = Field(default=None, primary_key=True)
    title: str
    notice_date: str
    notice_type: str
    record_num: int
    trigger_num: int
    grb_date: str
    grb_time: str
    trigger_signif: str
    trigger_dur: str
    e_range: str
    algorithm: str
    detectors: str
    lc_url: str
    comments: str
    observations: list["Observation"] = Relationship(back_populates="alert")
