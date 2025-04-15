from dataclasses import dataclass
from typing import List

@dataclass
class Event:
    id: any

@dataclass
class Client:
    id: any
    name: str
    events: List[Event]