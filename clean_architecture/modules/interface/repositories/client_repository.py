from dataclasses import dataclass
from typing import List
from clean_architecture.modules.entities import Client



@dataclass
class ClientRepository:
    data_base_repository: object

    def save(self, client: Client) -> Client:
        return self.data_base_repository.save(client)

    def get(self, client_id: int) -> Client:
        return self.data_base_repository.get(client_id)

    def delete(self, client_id: int) -> None:
        return self.data_base_repository.delete(client_id)

    def get_all(self, **kwargs) -> List[Client]:
        return self.data_base_repository.get_all(**kwargs)