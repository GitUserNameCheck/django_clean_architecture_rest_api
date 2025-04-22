import bson
from rest_framework.response import Response
from clean_architecture.modules.entities.ServiceEmployee import ServiceEmployee as ServiceEmployeeEntity
from clean_architecture.modules.entities.Employee import Employee as EmployeeEntity
from clean_architecture.modules.entities.Service import Service as ServiceEntity
from clean_architecture.modules.infrastructure.db_repo.service_employee_db_repository import ServiceEmployeeDbRepository
from clean_architecture.modules.usecases.repositories.service_employee_repository import ServiceEmployeeRepository
from clean_architecture.modules.interface.controllers.service_employee_controller import ServiceEmployeeController
from clean_architecture.modules.usecases.service_employee_use_cases import ServiceEmployeeUseCases
from rest_framework import serializers
from rest_framework import viewsets, status
from rest_framework.response import Response
import bson


class EmployeeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()

class ServiceSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    price = serializers.IntegerField()
    description = serializers.CharField()

class ServiceEmployeeSerializer(serializers.Serializer):
    id = serializers.CharField(required=False, allow_null=True)
    employee = EmployeeSerializer()
    service = ServiceSerializer()


service_employee_db_repo = ServiceEmployeeDbRepository()
service_employee_repo = ServiceEmployeeRepository(service_employee_db_repo)
service_employee_use_cases = ServiceEmployeeUseCases(service_employee_repo)
service_employee_controller = ServiceEmployeeController(service_employee_use_cases)

class ServiceEmployeeViewSet(viewsets.ViewSet):

    def list(self, request):
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 12))
        result = service_employee_controller.get_service_employees(page=page, per_page=per_page)

        serializer = ServiceEmployeeSerializer(result.object_list, many=True)

        response_data = {
            'count': result.paginator.count,
            'num_pages': result.paginator.num_pages,
            'current_page': result.number,
            'results': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            result = service_employee_controller.get_service_employee(pk)
            return Response(ServiceEmployeeSerializer(result).data, status=status.HTTP_200_OK)
        except bson.errors.InvalidId:
            return Response({"error": "Invalid service_employee ID"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = ServiceEmployeeSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            service_employee = ServiceEmployeeEntity(
                id=None,
                employee=EmployeeEntity(id=data["employee"]["id"], name=data["employee"]["name"]),
                service=ServiceEntity(id=data["service"]["id"], price=data["service"]["price"], description=data["service"]["description"])
            )
            result = service_employee_controller.create_service_employee(service_employee)
            return Response(ServiceEmployeeSerializer(result).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        serializer = ServiceEmployeeSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            service_employee = ServiceEmployeeEntity(
                id=pk,
                employee=EmployeeEntity(id=data["employee"]["id"], name=data["employee"]["name"]),
                service=ServiceEntity(id=data["service"]["id"], price=data["service"]["price"], description=data["service"]["description"])
            )
            try:
                result = service_employee_controller.update_service_employee(service_employee)
                return Response(ServiceEmployeeSerializer(result).data, status=status.HTTP_200_OK)
            except bson.errors.InvalidId:
                return Response({"error": "Invalid service_employee ID"}, status=status.HTTP_400_BAD_REQUEST)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            service_employee_controller.delete_service_employee(pk)
            return Response(status=status.HTTP_200_OK)
        except bson.errors.InvalidId:
            return Response({"error": "Invalid service_employee ID"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)