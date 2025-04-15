from django.db import models
from django_mongodb_backend.fields import EmbeddedModelField, ArrayField
from django_mongodb_backend.models import EmbeddedModel

class Client(EmbeddedModel):
    name = models.CharField(max_length=500, db_collation='Cyrillic_General_CI_AS', blank=True, null=True)

    def __str__(self):
         return str(self.id)
    
class Location(EmbeddedModel):
    id = models.IntegerField(default=0)
    address = models.CharField(max_length=500, db_collation='Cyrillic_General_CI_AS', blank=True, null=True)

    def __str__(self):
         return str(self.id)

class Event(models.Model):
    id = models.BigAutoField(primary_key=True)
    location = EmbeddedModelField(Location)
    client = EmbeddedModelField(Client)
    event_start = models.DateTimeField(blank=True, null=True)
    event_end = models.DateTimeField(blank=True, null=True)

    class Meta:
        app_label = 'clean_architecture'
        managed = False
        db_table = 'event'

    def __str__(self):
	    return str(self.id) + ': ' + str(self.client) + "; " + str(self.location) + "; " + str(self.event_start) + "; " + str(self.event_end)
