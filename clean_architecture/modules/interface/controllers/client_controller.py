from clean_architecture.modules.useсases.client_use_cases import ClientUseCases
from clean_architecture.modules.entities import Client



class ClientController:
    def __init__(self, client_use_cases: ClientUseCases):
        self.client_use_cases = client_use_cases

    def create_client(self, client: Client):
        return self.client_use_cases.create_client(client)
         
    def update_client(self, client: Client):
        return self.client_use_cases.update_client(client)

    def delete_client(self, client_id: any):
        self.client_use_cases.delete_client(client_id)
    
    def get_client(self, client_id: any):
        return self.client_use_cases.get_client(client_id)
        
    def get_clients(self, **kwargs):
        return self.client_use_cases.get_clients(**kwargs)
         