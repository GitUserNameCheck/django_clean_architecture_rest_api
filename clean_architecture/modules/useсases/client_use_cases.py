from typing import List
from dataclasses import dataclass
from clean_architecture.modules.entities import Client


@dataclass
class ClientUseCases:
    client_repository: object

    def create_client(self, client: Client) -> Client:
        return self.client_repository.save(client)

    def delete_client(self, client_id: any):
        return self.client_repository.delete(client_id)

    def update_client(self, updated_client: Client) -> Client:
        client = self.client_repository.get(updated_client.id)
        if not client:
            raise ValueError(f"Client with id {updated_client.id} not found.")
        return self.client_repository.save(updated_client)

    def view_clients(self, **kwargs) -> List[Client]:
        return self.client_repository.get_all(**kwargs)