from dataclasses import dataclass
from clean_architecture.modules.entities import ServiceEmployee



@dataclass
class ServiceEmployeeRepository:
    data_base_repository: object

    def save(self, service_employee: ServiceEmployee) -> ServiceEmployee:
        return self.data_base_repository.save(service_employee)

    def get(self, service_employee_id: any) -> ServiceEmployee:
        return self.data_base_repository.get(service_employee_id)

    def delete(self, service_employee_id: any):
        self.data_base_repository.delete(service_employee_id)

    def get_all(self, **kwargs):
        return self.data_base_repository.get_all(**kwargs)