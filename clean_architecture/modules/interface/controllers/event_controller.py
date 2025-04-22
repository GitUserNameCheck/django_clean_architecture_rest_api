from clean_architecture.modules.usecases.event_use_cases import EventUseCases
from clean_architecture.modules.entities import Event


class EventController:
    def __init__(self, event_use_cases: EventUseCases):
        self.event_use_cases = event_use_cases

    def create_event(self, event: Event):
        return self.event_use_cases.create_event(event)

    def update_event(self, event: Event):
        return self.event_use_cases.update_event(event)

    def delete_event(self, event_id: any):
        self.event_use_cases.delete_event(event_id)

    def get_event(self, event_id: any):
        return self.event_use_cases.get_event(event_id)

    def get_events(self, **kwargs):
        return self.event_use_cases.get_events(**kwargs)