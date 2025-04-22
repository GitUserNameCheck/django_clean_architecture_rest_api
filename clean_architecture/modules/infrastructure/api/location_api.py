import bson
from rest_framework.response import Response
from clean_architecture.modules.entities.Location import Location as LocationEntity
from clean_architecture.modules.infrastructure.db_repo.location_db_repository import LocationDbRepository
from clean_architecture.modules.usecases.repositories.location_repository import LocationRepository
from clean_architecture.modules.interface.controllers.location_controller import LocationController
from clean_architecture.modules.usecases.location_use_cases import LocationUseCases
from rest_framework import serializers
from rest_framework import viewsets, status
from rest_framework.response import Response
import bson



class LocationSerializer(serializers.Serializer):
    id = serializers.CharField(required=False, allow_null=True)
    address = serializers.CharField()


location_db_repo = LocationDbRepository()
location_repo = LocationRepository(location_db_repo)
location_use_cases = LocationUseCases(location_repo)
location_controller = LocationController(location_use_cases)

class LocationViewSet(viewsets.ViewSet):

    def list(self, request):
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 12))
        result = location_controller.get_locations(page=page, per_page=per_page)

        serializer = LocationSerializer(result.object_list, many=True)

        response_data = {
            'count': result.paginator.count,
            'num_pages': result.paginator.num_pages,
            'current_page': result.number,
            'results': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            result = location_controller.get_location(pk)
            return Response(LocationSerializer(result).data, status=status.HTTP_200_OK)
        except bson.errors.InvalidId:
            return Response({"error": "Invalid location ID"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            location = LocationEntity(
                id=None,
                address=data.get("address"),
            )
            result = location_controller.create_location(location)
            return Response(LocationSerializer(result).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            location = LocationEntity(
                id=pk,
                address=data.get("address"),
            )
            try:
                result = location_controller.update_location(location)
                return Response(LocationSerializer(result).data, status=status.HTTP_200_OK)
            except bson.errors.InvalidId:
                return Response({"error": "Invalid location ID"}, status=status.HTTP_400_BAD_REQUEST)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            location_controller.delete_location(pk)
            return Response(status=status.HTTP_200_OK)
        except bson.errors.InvalidId:
            return Response({"error": "Invalid location ID"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)