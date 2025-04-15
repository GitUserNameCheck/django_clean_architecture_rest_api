from dataclasses import dataclass
from typing import Optional
from . import Service, Employee


@dataclass
class ServiceEmployee:
    id: any
    service: Service
    employee: Employee