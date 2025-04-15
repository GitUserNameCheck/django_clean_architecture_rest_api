from typing import List
from dataclasses import dataclass
from clean_architecture.modules.entities import Employee


@dataclass
class EmployeeUseCases:
    employee_repository: object

    def create_employee(self, employee: Employee) -> Employee:
        return self.employee_repository.save(employee)

    def delete_employee(self, employee_id: any):
        return self.employee_repository.delete(employee_id)

    def update_employee(self, updated_employee: Employee) -> Employee:
        employee = self.employee_repository.get(updated_employee.id)
        if not employee:
            raise ValueError(f"Employee with id {updated_employee.id} not found.")
        return self.employee_repository.save(updated_employee)

    def view_employees(self, **kwargs) -> List[Employee]:
        return self.employee_repository.get_all(**kwargs)