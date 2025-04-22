from clean_architecture.modules.usecases.service_use_cases import ServiceUseCases
from clean_architecture.modules.entities import Service



class ServiceController:
    def __init__(self, service_use_cases: ServiceUseCases):
        self.service_use_cases = service_use_cases

    def create_service(self, service: Service):
        return self.service_use_cases.create_service(service)
         
    def update_service(self, service: Service):
        return self.service_use_cases.update_service(service)

    def delete_service(self, service_id: any):
        self.service_use_cases.delete_service(service_id)
    
    def get_service(self, service_id: any):
        return self.service_use_cases.get_service(service_id)
        
    def get_services(self, **kwargs):
        return self.service_use_cases.get_services(**kwargs)
         