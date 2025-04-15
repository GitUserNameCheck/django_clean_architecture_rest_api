from typing import List
from dataclasses import dataclass
from clean_architecture.modules.entities import Location


@dataclass
class LocationUseCases:
    location_repository: object

    def create_location(self, location: Location) -> Location:
        return self.location_repository.save(location)

    def delete_location(self, location_id: any):
        self.location_repository.delete(location_id)

    def update_location(self, updated_location: Location) -> Location:
        location = self.location_repository.get(updated_location.id)
        if not location:
            raise ValueError(f"Location with id {updated_location.id} not found.")
        return self.location_repository.save(updated_location)

    def get_location(self, location_id: any) -> Location:
        return self.location_repository.get(location_id)

    def get_locations(self, **kwargs) -> List[Location]:
        return self.location_repository.get_all(**kwargs)