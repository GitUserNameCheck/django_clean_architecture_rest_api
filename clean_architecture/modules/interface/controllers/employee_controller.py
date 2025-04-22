from clean_architecture.modules.usecases.employee_use_cases import EmployeeUseCases
from clean_architecture.modules.entities import Employee



class EmployeeController:
    def __init__(self, employee_use_cases: EmployeeUseCases):
        self.employee_use_cases = employee_use_cases

    def create_employee(self, employee: Employee):
        return self.employee_use_cases.create_employee(employee)
         
    def update_employee(self, employee: Employee):
        return self.employee_use_cases.update_employee(employee)

    def delete_employee(self, employee_id: any):
        self.employee_use_cases.delete_employee(employee_id)
    
    def get_employee(self, employee_id: any):
        return self.employee_use_cases.get_employee(employee_id)
        
    def get_employees(self, **kwargs):
        return self.employee_use_cases.get_employees(**kwargs)
         