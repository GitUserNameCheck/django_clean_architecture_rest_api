import bson
from rest_framework.response import Response
from clean_architecture.modules.entities.Client import Client as ClientEntity, Event as EventProxy
from clean_architecture.modules.infrastructure.db_repo.client_db_repository import ClientDbRepository
from clean_architecture.modules.usecases.repositories.client_repository import ClientRepository
from clean_architecture.modules.interface.controllers.client_controller import ClientController
from clean_architecture.modules.usecases.client_use_cases import ClientUseCases
from rest_framework import serializers
from rest_framework import viewsets, status
from rest_framework.response import Response
import bson

class EventSerializer(serializers.Serializer):
    id = serializers.CharField(required=True, allow_null=True)

class ClientSerializer(serializers.Serializer):
    id = serializers.CharField(required=False, allow_null=True)
    name = serializers.CharField()
    events = serializers.ListField(
        child=EventSerializer()
    )

client_db_repo = ClientDbRepository()
client_repo = ClientRepository(client_db_repo)
client_use_cases = ClientUseCases(client_repo)
client_controller = ClientController(client_use_cases)

class ClientViewSet(viewsets.ViewSet):

    def list(self, request):
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 12))
        result = client_controller.get_clients(page=page, per_page=per_page)

        serializer = ClientSerializer(result.object_list, many=True)

        response_data = {
            'count': result.paginator.count,
            'num_pages': result.paginator.num_pages,
            'current_page': result.number,
            'results': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            result = client_controller.get_client(pk)
            return Response(ClientSerializer(result).data, status=status.HTTP_200_OK)
        except bson.errors.InvalidId:
            return Response({"error": "Invalid client ID"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            client = ClientEntity(
                id=None,
                name=data.get("name"),
                # events = data.get("events", [])
                events=[EventProxy(id = event["id"]) for event in data.get("events", [])]
            )
            result = client_controller.create_client(client)
            return Response(ClientSerializer(result).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            client = ClientEntity(
                id=pk,
                name=data.get("name"),
                # events = data.get("events", [])
                events= [EventProxy(id = event["id"]) for event in data.get("events", [])]
            )
            try:
                result = client_controller.update_client(client)
                return Response(ClientSerializer(result).data, status=status.HTTP_200_OK)
            except bson.errors.InvalidId:
                return Response({"error": "Invalid client ID"}, status=status.HTTP_400_BAD_REQUEST)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            client_controller.delete_client(pk)
            return Response(status=status.HTTP_200_OK)
        except bson.errors.InvalidId:
            return Response({"error": "Invalid client ID"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)