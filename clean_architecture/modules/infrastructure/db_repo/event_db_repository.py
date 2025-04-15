from typing import List, Optional
from clean_architecture.modules.infrastructure.db import Location, Client, Event
from django.core.paginator import Paginator, EmptyPage
from datetime import datetime

class EventDbRepository:
    def save(self, event: Event) -> Event:
        event_model, _ = Event.objects.update_or_create(
            id=event.id,
            defaults={
                "location_id": event.location.id,
                "client_id": event.client.id,
                "event_start": event.event_start,
                "event_end": event.event_end
            }
        )
        return event

    def get(self, event_id: int) -> Event:
        event_model = Event.objects.filter(id=event_id).first()
        if not event_model:
            return None
        return Event(
            id=event_model.id,
            location=Location(id=event_model.location.id, address=event_model.location.address),
            client=Client(id=event_model.client.id, name=event_model.client.name),
            event_start=event_model.event_start,
            event_end=event_model.event_end
        )

    def delete(self, event_id: int) -> None:
        Event.objects.filter(id=event_id).delete()

    def get_all(self, page: int = 1, per_page: int = 12, queryset=None) -> List[Event]:

        if queryset is None:
            queryset = Event.objects.all().order_by('id')
        
        paginator = Paginator(queryset, per_page)

        try:
            page_obj = paginator.get_page(page)
        except EmptyPage:
            page_obj = paginator.get_page(1)

        return page_obj
    
    def get_by_location_and_time(self, location: Location, event_start: datetime, event_end: datetime, event_id: Optional[int] = None) -> List[Event]:
        event_query = Event.objects.filter(
            location_id=location.id,
            event_start__lt=event_end,
            event_end__gt=event_start
        )

        if event_id is not None:
            event_query = event_query.exclude(id=event_id)

        return [
            Event(
                id=event_model.id,
                location=Location(id=event_model.location.id, address=event_model.location.address),
                client=Client(id=event_model.client.id, name=event_model.client.name),
                event_start=event_model.event_start,
                event_end=event_model.event_end
            )
            for event_model in event_query
        ]