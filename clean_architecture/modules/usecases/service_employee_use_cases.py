from typing import List
from dataclasses import dataclass
from clean_architecture.modules.entities import ServiceEmployee
# from clean_architecture.modules.usecases.repositories.service_employee_repository import ServiceEmployeeRepository

@dataclass
class ServiceEmployeeUseCases:
    service_employee_repository: object

    def create_service_employee(self, service_employee: ServiceEmployee) -> ServiceEmployee:
        return self.service_employee_repository.save(service_employee)

    def delete_service_employee(self, service_employee_id: any):
        self.service_employee_repository.delete(service_employee_id)

    def update_service_employee(self, updated_service_employee: ServiceEmployee) -> ServiceEmployee:
        service_employee = self.service_employee_repository.get(updated_service_employee.id)
        if not service_employee:
            raise ValueError(f"ServiceEmployee with id {updated_service_employee.id} not found.")
        return self.service_employee_repository.save(updated_service_employee)

    def get_service_employee(self, service_employee_id: any) -> ServiceEmployee:
        return self.service_employee_repository.get(service_employee_id)

    def get_service_employees(self, **kwargs) -> List[ServiceEmployee]:
        return self.service_employee_repository.get_all(**kwargs)
