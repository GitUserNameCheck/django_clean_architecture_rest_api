from clean_architecture.modules.infrastructure.db_models.Employee import Employee as EmployeeModel
from clean_architecture.modules.entities.Employee import Employee as EmployeeEntity
from django.core.paginator import Paginator, EmptyPage

class EmployeeDbRepository:
    def save(self, employee: EmployeeEntity) -> EmployeeEntity:
        employee_model, _ = EmployeeModel.objects.update_or_create(
            id=employee.id,
            defaults={"name": employee.name}
        )
        employee.id = employee_model.id
        return employee

    def get(self, employee_id: any) -> EmployeeEntity:
        employee_model = EmployeeModel.objects.filter(pk=employee_id).first()
        if not employee_model:
            return None
        return EmployeeEntity(id=employee_model.id, name=employee_model.name)

    def delete(self, employee_id: any) -> None:
        EmployeeModel.objects.filter(id=employee_id).delete()

    def get_all(self, page: int = 1, per_page: int = 12, queryset=None):
        
        if queryset is None:
            queryset = EmployeeModel.objects.all().order_by('id')

        paginator = Paginator(queryset, per_page)

        try:
            page_obj = paginator.get_page(page)
        except EmptyPage:
            page_obj = paginator.get_page(1)

        return page_obj
