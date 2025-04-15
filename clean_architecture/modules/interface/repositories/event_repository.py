from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from clean_architecture.modules.entities import Location, Event



@dataclass
class EventRepository:
    data_base_repository: object

    def save(self, event: Event) -> Event:
        return self.data_base_repository.save(event)

    def get(self, event_id: int) -> Event:
        return self.data_base_repository.get(event_id)

    def delete(self, event: int) -> None:
        return self.data_base_repository.delete(event)

    def get_all(self, **kwargs) -> List[Event]:
        return self.data_base_repository.get_all(**kwargs)

    def get_by_location_and_time(self, location: Location, event_start: datetime, event_end: datetime, event_id: Optional[int] = None) -> List[Event]:
        return self.data_base_repository.get_by_location_and_time(location, event_start, event_end, event_id)