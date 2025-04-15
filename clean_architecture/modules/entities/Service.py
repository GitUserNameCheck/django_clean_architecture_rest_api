from dataclasses import dataclass
from typing import Optional

@dataclass
class Service:
    id: any
    price: int
    description: str
