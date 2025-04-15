from datetime import datetime
from http import HTTPStatus
from typing import Tuple, Dict

from clean_architecture.modules.useсases.event_use_cases import EventUseCases
from clean_architecture.modules.entities import Event


class EventController:
    def __init__(self, event_use_cases: EventUseCases):
        self.event_use_cases = event_use_cases

    def create_event(self, event: Event) -> Tuple[Dict, int]:
        try:
            event = self.event_use_cases.create_event(event)
            return {"message": "Event created successfully", "event": vars(event)}, HTTPStatus.CREATED.value
        except ValueError as e:
            return {"error": str(e)}, HTTPStatus.BAD_REQUEST.value

    def update_event(self, event: Event) -> Tuple[Dict, int]:
        try:
            event = self.event_use_cases.update_event(event)
            return {"message": "Event updated successfully", "event": vars(event)}, HTTPStatus.OK.value
        except ValueError as e:
            return {"error": str(e)}, HTTPStatus.BAD_REQUEST.value

    def delete_event(self, event_id: int) -> Tuple[Dict, int]:
        self.event_use_cases.delete_event(event_id)
        return {"message": "Event deleted successfully"}, HTTPStatus.NO_CONTENT.value

    def view_events(self, **kwargs) -> Tuple[Dict, int]:
        events = self.event_use_cases.view_events(**kwargs)
        return {"events": events}, HTTPStatus.OK.value