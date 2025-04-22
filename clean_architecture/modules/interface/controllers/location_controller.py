from clean_architecture.modules.usecases.location_use_cases import LocationUseCases
from clean_architecture.modules.entities import Location



class LocationController:
    def __init__(self, location_use_cases: LocationUseCases):
        self.location_use_cases = location_use_cases

    def create_location(self, location: Location):
        return self.location_use_cases.create_location(location)
         
    def update_location(self, location: Location):
        return self.location_use_cases.update_location(location)

    def delete_location(self, location_id: any):
        self.location_use_cases.delete_location(location_id)
    
    def get_location(self, location_id: any):
        return self.location_use_cases.get_location(location_id)
        
    def get_locations(self, **kwargs):
        return self.location_use_cases.get_locations(**kwargs)
         