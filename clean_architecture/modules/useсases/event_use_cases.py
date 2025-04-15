from typing import List, Optional
from datetime import datetime
from dataclasses import dataclass
from clean_architecture.modules.entities import Location, Event

@dataclass
class EventUseCases:
    event_repository: object
    
    def create_event(self, event: Event) -> Event:
        if self._is_event_conflict(event.location, event.event_start, event.event_end):
            raise ValueError("An event is already scheduled at this location during the specified time.")
        return self.event_repository.save(event)

    def delete_event(self, event_id: any):
        self.event_repository.delete(event_id)

    def update_event(self, updated_event: Event) -> Event:
        event = self.event_repository.get(updated_event.id)
        if not event:
            raise ValueError(f"Event with id {event.id} not found.")
        if self._is_event_conflict(updated_event.location, updated_event.event_start, updated_event.event_end, updated_event.id):
            raise ValueError("An event is already scheduled at this location during the specified time.")
        return self.event_repository.save(updated_event)

    def get_event(self, event_id: any) -> Event:
        return self.event_repository.get(event_id)

    def get_events(self, **kwargs) -> List[Event]:
        return self.event_repository.get_all(**kwargs)

    def _is_event_conflict(self, location: Location, event_start: datetime, event_end: datetime, event_id: Optional[any] = None) -> bool:
        events = self.event_repository.get_by_location_and_time(location, event_start, event_end, event_id)
        return len(events) > 0