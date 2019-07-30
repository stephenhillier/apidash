"""
Monitors API pydantic models
"""
from pydantic import BaseModel, UrlStr

class MonitorRequest(BaseModel):
    """ a request for a new monitor, which must include a name and an endpoint """
    name: str
    endpoint: UrlStr


class Monitor(BaseModel):
    """ a monitor represents a re-occuring check against an endpoint """
    id: int
    name: str
    endpoint: str
    status: int = 1

    class Config:
        orm_mode = True
