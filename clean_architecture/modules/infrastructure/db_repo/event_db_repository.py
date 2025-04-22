from typing import List, Optional
from clean_architecture.modules.infrastructure.db_models.Event import Event as EventModel, ClientProxy as ClientProxyModel
from clean_architecture.modules.infrastructure.db_models.Location import Location as LocationModel
from clean_architecture.modules.entities.Event import Event as EventEntity, ServiceEmployee as ServiceEmployeeProxy
from clean_architecture.modules.entities.Location import Location as LocationEntity
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage
from bson import ObjectId

class EventDbRepository:
    def save(self, event: EventEntity) -> EventEntity:
        event_model, _ = EventModel.objects.update_or_create(
            _id=ObjectId(event.id),
            defaults={"location": LocationModel(id=event.location.id, 
                                                address=event.location.address), 
                      "client": ClientProxyModel(_id=event.client.id,
                                                name=event.client.name),
                      "event_start": event.event_start,
                      "event_end": event.event_end,
                      "service_employees": [service_employee.id for service_employee in event.service_employees]
                    }
        )
        event.id = event_model._id
        return event

    def get(self, event_id: any) -> EventEntity:
        event_model = EventModel.objects.filter(pk=event_id).first()
        if not event_model:
            return None
        service_employees = []
        event_model.client.id = event_model.client._id
        for service_employee in event_model.service_employees:
            service_employees.append(ServiceEmployeeProxy(service_employee))
        return EventEntity(id=event_model._id, location=event_model.location, client=event_model.client,
                           event_start=event_model.event_start, event_end=event_model.event_end,
                           service_employees=service_employees)

    def delete(self, event_id: any) -> None:
        EventModel.objects.filter(_id=event_id).delete()

    def get_all(self, page: int = 1, per_page: int = 12, queryset=None):
        
        if queryset is None:
            queryset = EventModel.objects.all().order_by('_id')

        paginator = Paginator(queryset, per_page)

        try:
            page_obj = paginator.get_page(page)
        except EmptyPage:
            page_obj = paginator.get_page(1)

        for event in page_obj.object_list:
            event.id = event._id
            event.client.id = event.client._id
            service_employees = []
            for service_employee in event.service_employees:
                service_employees.append(ServiceEmployeeProxy(service_employee))
            event.service_employees = service_employees

        return page_obj
    
    def get_by_location_and_time(self, location: LocationEntity, event_start: datetime, event_end: datetime, event_id: Optional[int] = None) -> List[EventEntity]:
        event_query = EventModel.objects.filter(
            location__id=location.id,
            event_start__lt=event_end,
            event_end__gt=event_start
        )

        if event_id is not None:
            event_query = event_query.exclude(_id=event_id)

        events = []
        for event_model in event_query:
            event_model.client.id = event_model.client._id
            events.append(EventEntity(
                        id=event_model._id,
                        # location=Location(id=event_model.location.id, address=event_model.location.address),
                        location=event_model.location,
                        # client=Client(id=event_model.client.id, name=event_model.client.name),
                        client=event_model.client,
                        event_start=event_model.event_start,
                        event_end=event_model.event_end,
                        service_employees=event_model.service_employees
                    ))

        return events
