from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime
from . import Location

@dataclass
class Client:
    id: any
    name: str

@dataclass
class ServiceEmployee:
    id: any

@dataclass
class Event:
    id: any
    location: Location
    client: Client
    event_start: Optional[datetime]
    event_end: Optional[datetime]
    service_employees: List[ServiceEmployee]
