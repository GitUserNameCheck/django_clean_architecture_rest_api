from clean_architecture.modules.infrastructure.db_models.Service import Service as ServiceModel
from clean_architecture.modules.entities.Service import Service as ServiceEntity
from django.core.paginator import Paginator, EmptyPage

class ServiceDbRepository:
    def save(self, service: ServiceEntity) -> ServiceEntity:
        service_model, _ = ServiceModel.objects.update_or_create(
            id=service.id,
            defaults={"price": service.price, "description": service.description}
        )
        service.id = service_model.id
        return service

    def get(self, service_id: any) -> ServiceEntity:
        service_model = ServiceModel.objects.filter(pk=service_id).first()
        if not service_model:
            return None
        return ServiceEntity(id=service_model.id, price=service_model.price, description=service_model.description)

    def delete(self, service_id: any) -> None:
        ServiceModel.objects.filter(id=service_id).delete()

    def get_all(self, page: int = 1, per_page: int = 12, queryset=None):
        
        if queryset is None:
            queryset = ServiceModel.objects.all().order_by('id')

        paginator = Paginator(queryset, per_page)

        try:
            page_obj = paginator.get_page(page)
        except EmptyPage:
            page_obj = paginator.get_page(1)

        return page_obj
