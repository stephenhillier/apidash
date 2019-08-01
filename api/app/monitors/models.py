"""
Monitors API pydantic models
"""
from datetime import datetime, date
from pydantic import BaseModel, UrlStr
from typing import Optional, List


class MonitorRequest(BaseModel):
    """ a request for a new monitor, which must include a name and an endpoint """
    name: str
    endpoint: UrlStr


class DailySummary(BaseModel):
    """ a summary of a day's worth of checks for an endpoint monitor """
    date: date
    num_ok: int
    num_fail: int


class Monitor(BaseModel):
    """ a monitor represents a re-occuring check against an endpoint """
    id: int
    name: str
    endpoint: str
    current_status: int = 1
    last_failed: Optional[datetime]
    last_checked: Optional[datetime]
    last_success: Optional[datetime]
    weekly: List[DailySummary] = []

    class Config:
        orm_mode = True
