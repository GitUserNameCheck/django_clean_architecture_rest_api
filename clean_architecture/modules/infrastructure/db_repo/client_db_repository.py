from clean_architecture.modules.infrastructure.db.Client import Client as ClientModel
from clean_architecture.modules.entities.Client import Client as ClientEntity, Event as EventProxy
from django.core.paginator import Paginator, EmptyPage
from bson import ObjectId

class ClientDbRepository:
    def save(self, client: ClientEntity) -> ClientEntity:
        client_model, _ = ClientModel.objects.update_or_create(
            _id=ObjectId(client.id),
            defaults={"name": client.name, "events": [event.id for event in client.events]}
        )
        client.id = client_model._id
        return client

    def get(self, client_id: any) -> ClientEntity:
        client_model = ClientModel.objects.filter(pk=client_id).first()
        if not client_model:
            return None
        events = []
        for event in client_model.events:
            events.append(EventProxy(event))
        return ClientEntity(id=client_model._id, name=client_model.name, events=events)

    def delete(self, client_id: any) -> None:
        ClientModel.objects.filter(_id=client_id).delete()

    def get_all(self, page: int = 1, per_page: int = 12, queryset=None):
        
        if queryset is None:
            queryset = ClientModel.objects.all().order_by('_id')

        paginator = Paginator(queryset, per_page)

        try:
            page_obj = paginator.get_page(page)
        except EmptyPage:
            page_obj = paginator.get_page(1)

        for client in page_obj.object_list:
            client.id = client._id
            events = []
            for event in client.events:
                events.append(EventProxy(event))
            client.events = events

        return page_obj
