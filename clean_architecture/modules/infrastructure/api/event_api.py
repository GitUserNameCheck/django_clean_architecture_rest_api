import bson
from rest_framework.response import Response
from clean_architecture.modules.entities.Event import Event as EventEntity, Client as ClientProxy, ServiceEmployee as ServiceEmployeeProxy
from clean_architecture.modules.entities.Location import Location as LocationEntity
from clean_architecture.modules.infrastructure.db_repo.event_db_repository import EventDbRepository
from clean_architecture.modules.usecases.repositories.event_repository import EventRepository
from clean_architecture.modules.interface.controllers.event_controller import EventController
from clean_architecture.modules.usecases.event_use_cases import EventUseCases
from datetime import datetime
from rest_framework import serializers
from rest_framework import viewsets, status
from rest_framework.response import Response
import bson


class ServiceEmployeeSerializer(serializers.Serializer):
    id = serializers.CharField(required=True, allow_null=True)

class ClientSerializer(serializers.Serializer):
    id = serializers.CharField(required=False, allow_null=True)
    name = serializers.CharField()

class LocationSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    address = serializers.CharField()

class EventSerializer(serializers.Serializer):
    id = serializers.CharField(required=False, allow_null=True)
    location = LocationSerializer()
    client = ClientSerializer()
    event_start = serializers.DateTimeField()
    event_end = serializers.DateTimeField()
    service_employees = serializers.ListField(
        child=ServiceEmployeeSerializer()
    )


event_db_repo = EventDbRepository()
event_repo = EventRepository(event_db_repo)
event_use_cases = EventUseCases(event_repo)
event_controller = EventController(event_use_cases)

class EventViewSet(viewsets.ViewSet):

    def list(self, request):
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 12))
        result = event_controller.get_events(page=page, per_page=per_page)

        serializer = EventSerializer(result.object_list, many=True)

        response_data = {
            'count': result.paginator.count,
            'num_pages': result.paginator.num_pages,
            'current_page': result.number,
            'results': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            result = event_controller.get_event(pk)
            return Response(EventSerializer(result).data, status=status.HTTP_200_OK)
        except bson.errors.InvalidId:
            return Response({"error": "Invalid event ID"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            event = EventEntity(
                id=None,
                location = LocationEntity(id=data["location"]["id"], address=data["location"]["address"]),
                client = ClientProxy(id=data["client"]["id"], name=data["client"]["name"]),
                event_start=data["event_start"],
                event_end=data["event_end"],
                service_employees=[ServiceEmployeeProxy(id = service_employee["id"]) for service_employee in data.get("service_employees", [])]
            )
            result = event_controller.create_event(event)
            return Response(EventSerializer(result).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            event = EventEntity(
                id=pk,
                location = LocationEntity(id=data["location"]["id"], address=data["location"]["address"]),
                client = ClientProxy(id=data["client"]["id"], name=data["client"]["name"]),
                event_start=data["event_start"],
                event_end=data["event_end"],
                service_employees=[ServiceEmployeeProxy(id = service_employee["id"]) for service_employee in data.get("service_employees", [])]
            )
            try:
                result = event_controller.update_event(event)
                return Response(EventSerializer(result).data, status=status.HTTP_200_OK)
            except bson.errors.InvalidId:
                return Response({"error": "Invalid event ID"}, status=status.HTTP_400_BAD_REQUEST)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            event_controller.delete_event(pk)
            return Response(status=status.HTTP_200_OK)
        except bson.errors.InvalidId:
            return Response({"error": "Invalid event ID"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)