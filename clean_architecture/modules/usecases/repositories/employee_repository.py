from dataclasses import dataclass
from clean_architecture.modules.entities import Employee



@dataclass
class EmployeeRepository:
    data_base_repository: object

    def save(self, employee: Employee) -> Employee:
        return self.data_base_repository.save(employee)

    def get(self, employee_id: any) -> Employee:
        return self.data_base_repository.get(employee_id)

    def delete(self, employee_id: any):
        self.data_base_repository.delete(employee_id)

    def get_all(self, **kwargs):
        return self.data_base_repository.get_all(**kwargs)