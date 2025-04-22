from dataclasses import dataclass
from clean_architecture.modules.entities import Service



@dataclass
class ServiceRepository:
    data_base_repository: object

    def save(self, service: Service) -> Service:
        return self.data_base_repository.save(service)

    def get(self, service_id: any) -> Service:
        return self.data_base_repository.get(service_id)

    def delete(self, service_id: any):
        self.data_base_repository.delete(service_id)

    def get_all(self, **kwargs):
        return self.data_base_repository.get_all(**kwargs)