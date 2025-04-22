from dataclasses import dataclass
from clean_architecture.modules.entities import Location



@dataclass
class LocationRepository:
    data_base_repository: object

    def save(self, location: Location) -> Location:
        return self.data_base_repository.save(location)

    def get(self, location_id: any) -> Location:
        return self.data_base_repository.get(location_id)

    def delete(self, location_id: any):
        self.data_base_repository.delete(location_id)

    def get_all(self, **kwargs):
        return self.data_base_repository.get_all(**kwargs)