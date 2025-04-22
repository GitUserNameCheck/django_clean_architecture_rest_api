from django.db import models
from django_mongodb_backend.models import EmbeddedModel
from clean_architecture.modules.infrastructure.db_models import Location
from django_mongodb_backend.fields import ObjectIdField, ArrayField, EmbeddedModelField

class ClientProxy(EmbeddedModel):
    _id = ObjectIdField(primary_key=True)
    name = models.CharField(max_length=500, db_collation='Cyrillic_General_CI_AS', blank=True, null=True)

    class Meta:
        app_label = 'clean_architecture'

    def __str__(self):
         return str(self.id)
    
class Event(models.Model):
    _id = ObjectIdField(primary_key=True)
    location = EmbeddedModelField(Location)
    client = EmbeddedModelField(ClientProxy)
    event_start = models.DateTimeField(blank=True, null=True)
    event_end = models.DateTimeField(blank=True, null=True)
    service_employees = ArrayField(models.CharField(max_length=24), null=True, blank=True)

    class Meta:
        app_label = 'clean_architecture'
        managed = False
        db_table = 'event'

    def __str__(self):
	    return str(self.id) + ': ' + str(self.client) + "; " + str(self.location) + "; " + str(self.event_start) + "; " + str(self.event_end)
