import bson
from rest_framework.response import Response
from clean_architecture.modules.entities.Service import Service as ServiceEntity
from clean_architecture.modules.infrastructure.db_repo.service_db_repository import ServiceDbRepository
from clean_architecture.modules.usecases.repositories.service_repository import ServiceRepository
from clean_architecture.modules.interface.controllers.service_controller import ServiceController
from clean_architecture.modules.usecases.service_use_cases import ServiceUseCases
from rest_framework import serializers
from rest_framework import viewsets, status
from rest_framework.response import Response
import bson



class ServiceSerializer(serializers.Serializer):
    id = serializers.CharField(required=False, allow_null=True)
    price = serializers.IntegerField()
    description = serializers.CharField()


service_db_repo = ServiceDbRepository()
service_repo = ServiceRepository(service_db_repo)
service_use_cases = ServiceUseCases(service_repo)
service_controller = ServiceController(service_use_cases)

class ServiceViewSet(viewsets.ViewSet):

    def list(self, request):
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 12))
        result = service_controller.get_services(page=page, per_page=per_page)

        serializer = ServiceSerializer(result.object_list, many=True)

        response_data = {
            'count': result.paginator.count,
            'num_pages': result.paginator.num_pages,
            'current_page': result.number,
            'results': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            result = service_controller.get_service(pk)
            return Response(ServiceSerializer(result).data, status=status.HTTP_200_OK)
        except bson.errors.InvalidId:
            return Response({"error": "Invalid service ID"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            service = ServiceEntity(
                id=None,
                price=data.get("price"),
                description=data.get("description")
            )
            result = service_controller.create_service(service)
            return Response(ServiceSerializer(result).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            service = ServiceEntity(
                id=pk,
                price=data.get("price"),
                description=data.get("description")
            )
            try:
                result = service_controller.update_service(service)
                return Response(ServiceSerializer(result).data, status=status.HTTP_200_OK)
            except bson.errors.InvalidId:
                return Response({"error": "Invalid service ID"}, status=status.HTTP_400_BAD_REQUEST)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            service_controller.delete_service(pk)
            return Response(status=status.HTTP_200_OK)
        except bson.errors.InvalidId:
            return Response({"error": "Invalid service ID"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)