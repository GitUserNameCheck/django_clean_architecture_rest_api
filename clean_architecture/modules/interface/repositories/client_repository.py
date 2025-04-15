from dataclasses import dataclass
from typing import List
from clean_architecture.modules.entities import Client



@dataclass
class ClientRepository:
    data_base_repository: object

    def save(self, client: Client) -> Client:
        return self.data_base_repository.save(client)

    def get(self, client_id: any) -> Client:
        return self.data_base_repository.get(client_id)

    def delete(self, client_id: any):
        self.data_base_repository.delete(client_id)

    def get_all(self, **kwargs):
        return self.data_base_repository.get_all(**kwargs)