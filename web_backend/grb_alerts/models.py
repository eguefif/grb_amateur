from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from observations.models import Observation


class GRBAlert(SQLModel, table=True):
    __tablename__ = "grb_alerts"

    id: int | None = Field(default=None, primary_key=True)
    title: str | None
    notice_date: str | None
    notice_type: str | None
    record_num: int | None
    trigger_num: int | None
    grb_date: str | None
    grb_time: str | None
    trigger_signif: str | None
    trigger_dur: str | None
    e_range: str | None
    algorithm: str | None
    detectors: str | None
    lc_url: str | None
    comments: str | None
    observations: list["Observation"] = Relationship(back_populates="alert")


class GRBPosition(SQLModel, table=True):
    __tablename__ = "grb_positions"

    id: int | None = Field(default=None, primary_key=True)
    title: str
    notice_date: str
    notice_type: str
    record_num: int
    trigger_num: int
    grb_ra: str
    grb_dec: str
    grb_error: str
    grb_inten: str
    data_signif: str
    integ_time: str
    grb_date: str
    grb_time: str
    grb_phi: str
    grb_theta: str
    data_time_scale: str
    hard_ratio: str
    loc_algorithm: str
    most_likely: str
    second_most_likely: str
    detectors: str
    sun_dist: str
    moon_postn: str
    moon_dist: str
    moon_illum: str
    gal_coords: str
    ecl_coords: str
    comments: str
