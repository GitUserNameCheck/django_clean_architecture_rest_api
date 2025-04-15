from typing import List, Optional
from clean_architecture.modules.infrastructure.db import Client
from django.core.paginator import Paginator, EmptyPage


class ClientDbRepository:
    def save(self, client: Client) -> Client:
        client_model, _ = Client.objects.update_or_create(
            id=client.id,
            defaults={"name": client.name}
        )
        return client

    def get(self, client_id: int) -> Client:
        client_model = Client.objects.filter(id=client_id).first()
        if not client_model:
            return None
        return Client(id=client_model.id, name=client_model.name)

    def delete(self, client_id: int) -> None:
        Client.objects.filter(id=client_id).delete()

    def get_all(self, page: int = 1, per_page: int = 12, queryset=None) -> List[Client]:

        if queryset is None:
            queryset = Client.objects.all().order_by('id')

        paginator = Paginator(queryset, per_page)

        try:
            page_obj = paginator.get_page(page)
        except EmptyPage:
            page_obj = paginator.get_page(1)

        return page_obj
