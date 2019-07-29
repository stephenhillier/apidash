"""
Monitors API pydantic models
"""
from pydantic import BaseModel

class MonitorRequest(BaseModel):
    """ a request for a new monitor, which must include a name and an endpoint """
    name: str
    endpoint: str


class Monitor(BaseModel):
    """ a monitor represents a re-occuring check against an endpoint """
    id: int
    name: str
    endpoint: str
