from clean_architecture.modules.infrastructure.db_models.Location import Location as LocationModel
from clean_architecture.modules.entities.Location import Location as LocationEntity
from django.core.paginator import Paginator, EmptyPage

class LocationDbRepository:
    def save(self, location: LocationEntity) -> LocationEntity:
        location_model, _ = LocationModel.objects.update_or_create(
            id=location.id,
            defaults={"address": location.address}
        )
        location.id = location_model.id
        return location

    def get(self, location_id: any) -> LocationEntity:
        location_model = LocationModel.objects.filter(pk=location_id).first()
        if not location_model:
            return None
        return LocationEntity(id=location_model.id, address=location_model.address)

    def delete(self, location_id: any) -> None:
        LocationModel.objects.filter(id=location_id).delete()

    def get_all(self, page: int = 1, per_page: int = 12, queryset=None):
        
        if queryset is None:
            queryset = LocationModel.objects.all().order_by('id')

        paginator = Paginator(queryset, per_page)

        try:
            page_obj = paginator.get_page(page)
        except EmptyPage:
            page_obj = paginator.get_page(1)

        return page_obj
