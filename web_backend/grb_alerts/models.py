from sqlmodel import SQLModel

class GRBAlert(SQLModel, table=True):
    __table__name = 'grb_alerts'

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
    comments: list[str]
