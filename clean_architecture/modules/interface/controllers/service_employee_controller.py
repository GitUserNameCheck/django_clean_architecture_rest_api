from clean_architecture.modules.usecases.service_employee_use_cases import ServiceEmployeeUseCases
from clean_architecture.modules.entities import ServiceEmployee



class ServiceEmployeeController:
    def __init__(self, service_employee_use_cases: ServiceEmployeeUseCases):
        self.service_employee_use_cases = service_employee_use_cases

    def create_service_employee(self, service_employee: ServiceEmployee):
        return self.service_employee_use_cases.create_service_employee(service_employee)
         
    def update_service_employee(self, service_employee: ServiceEmployee):
        return self.service_employee_use_cases.update_service_employee(service_employee)

    def delete_service_employee(self, service_employee_id: any):
        self.service_employee_use_cases.delete_service_employee(service_employee_id)
    
    def get_service_employee(self, service_employee_id: any):
        return self.service_employee_use_cases.get_service_employee(service_employee_id)
        
    def get_service_employees(self, **kwargs):
        return self.service_employee_use_cases.get_service_employees(**kwargs)
         