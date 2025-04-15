from http import HTTPStatus
from typing import Tuple, Dict

from clean_architecture.modules.useсases.client_use_cases import ClientUseCases
from clean_architecture.modules.entities import Client



class ClientController:
    def __init__(self, client_use_cases: ClientUseCases):
        self.client_use_cases = client_use_cases

    def create_client(self, client: Client) -> Tuple[Dict, int]:
        client = self.client_use_cases.create_client(client)
        return {"message": "Client created successfully", "client": vars(client)}, HTTPStatus.CREATED.value

    def update_client(self, client: Client) -> Tuple[Dict, int]:
        try:
            client = self.client_use_cases.update_client(client)
            return {"message": "Client updated successfully", "client": vars(client)}, HTTPStatus.OK.value
        except ValueError as e:
            return {"error": str(e)}, HTTPStatus.BAD_REQUEST.value

    def delete_client(self, client_id: int) -> Tuple[Dict, int]:
        self.client_use_cases.delete_client(client_id)
        return {"message": "Client deleted successfully"}, HTTPStatus.NO_CONTENT.value

    def view_clients(self, **kwargs) -> Tuple[Dict, int]:
        clients = self.client_use_cases.view_clients(**kwargs)
        return {"clients": clients}, HTTPStatus.OK.value