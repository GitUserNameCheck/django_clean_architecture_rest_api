from clean_architecture.modules.infrastructure.db_models.ServiceEmployee import ServiceEmployee as ServiceEmployeeModel
from clean_architecture.modules.infrastructure.db_models.Service import Service as ServiceModel
from clean_architecture.modules.infrastructure.db_models.Employee import Employee as EmployeeModel
from clean_architecture.modules.entities.ServiceEmployee import ServiceEmployee as ServiceEmployeeEntity
from django.core.paginator import Paginator, EmptyPage
from bson import ObjectId

class ServiceEmployeeDbRepository:
    def save(self, service_employee: ServiceEmployeeEntity) -> ServiceEmployeeEntity:
        service_employee_model, _ = ServiceEmployeeModel.objects.update_or_create(
            _id=ObjectId(service_employee.id),
            defaults={"employee": EmployeeModel(id=service_employee.employee.id, 
                                                name=service_employee.employee.name), 
                      "service": ServiceModel(id=service_employee.service.id,
                                              price=service_employee.service.price,
                                              description=service_employee.service.description),
                    }
        )
        service_employee.id = service_employee_model._id
        return service_employee

    def get(self, service_employee_id: any) -> ServiceEmployeeEntity:
        service_employee_model = ServiceEmployeeModel.objects.filter(pk=service_employee_id).first()
        if not service_employee_model:
            return None
        return ServiceEmployeeEntity(id=service_employee_model._id, employee=service_employee_model.employee, service=service_employee_model.service)

    def delete(self, service_employee_id: any) -> None:
        ServiceEmployeeModel.objects.filter(_id=service_employee_id).delete()

    def get_all(self, page: int = 1, per_page: int = 12, queryset=None):
        
        if queryset is None:
            queryset = ServiceEmployeeModel.objects.all().order_by('_id')

        paginator = Paginator(queryset, per_page)

        try:
            page_obj = paginator.get_page(page)
        except EmptyPage:
            page_obj = paginator.get_page(1)

        for service_employee in page_obj.object_list:
            service_employee.id = service_employee._id

        return page_obj
