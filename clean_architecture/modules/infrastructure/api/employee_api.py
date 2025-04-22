import bson
from rest_framework.response import Response
from clean_architecture.modules.entities.Employee import Employee as EmployeeEntity
from clean_architecture.modules.infrastructure.db_repo.employee_db_repository import EmployeeDbRepository
from clean_architecture.modules.usecases.repositories.employee_repository import EmployeeRepository
from clean_architecture.modules.interface.controllers.employee_controller import EmployeeController
from clean_architecture.modules.usecases.employee_use_cases import EmployeeUseCases
from rest_framework import serializers
from rest_framework import viewsets, status
from rest_framework.response import Response
import bson



class EmployeeSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    name = serializers.CharField()


employee_db_repo = EmployeeDbRepository()
employee_repo = EmployeeRepository(employee_db_repo)
employee_use_cases = EmployeeUseCases(employee_repo)
employee_controller = EmployeeController(employee_use_cases)

class EmployeeViewSet(viewsets.ViewSet):

    def list(self, request):
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 12))
        result = employee_controller.get_employees(page=page, per_page=per_page)

        serializer = EmployeeSerializer(result.object_list, many=True)

        response_data = {
            'count': result.paginator.count,
            'num_pages': result.paginator.num_pages,
            'current_page': result.number,
            'results': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            result = employee_controller.get_employee(pk)
            return Response(EmployeeSerializer(result).data, status=status.HTTP_200_OK)
        except bson.errors.InvalidId:
            return Response({"error": "Invalid employee ID"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            employee = EmployeeEntity(
                id=None,
                name=data.get("name"),
            )
            result = employee_controller.create_employee(employee)
            return Response(EmployeeSerializer(result).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            employee = EmployeeEntity(
                id=pk,
                name=data.get("name"),
            )
            try:
                result = employee_controller.update_employee(employee)
                return Response(EmployeeSerializer(result).data, status=status.HTTP_200_OK)
            except bson.errors.InvalidId:
                return Response({"error": "Invalid employee ID"}, status=status.HTTP_400_BAD_REQUEST)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            employee_controller.delete_employee(pk)
            return Response(status=status.HTTP_200_OK)
        except bson.errors.InvalidId:
            return Response({"error": "Invalid employee ID"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)