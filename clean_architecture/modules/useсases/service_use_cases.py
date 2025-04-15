from typing import List
from dataclasses import dataclass
from clean_architecture.modules.entities import Service


@dataclass
class ServiceUseCases:
    service_repository: object

    def create_service(self, service: Service) -> Service:
        return self.service_repository.save(service)

    def delete_service(self, service_id: any):
        return self.service_repository.delete(service_id)

    def update_service(self, updated_service: Service) -> Service:
        service = self.service_repository.get(updated_service.id)
        if not service:
            raise ValueError(f"Service with id {updated_service.id} not found.")
        return self.service_repository.save(updated_service)

    def view_services(self, **kwargs) -> List[Service]:
        return self.service_repository.get_all(**kwargs)