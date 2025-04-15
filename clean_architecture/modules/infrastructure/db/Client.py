from django.db import models
from django_mongodb_backend.fields import EmbeddedModelField, ArrayField
from django_mongodb_backend.models import EmbeddedModel


class Event(EmbeddedModel):
    def __str__(self):
         return str(self.id)

class Client(models.Model):
    name = models.CharField(max_length=500, db_collation='Cyrillic_General_CI_AS', blank=True, null=True)
    events = ArrayField(EmbeddedModelField(Event), null=True, blank=True)

    class Meta:
        app_label = 'clean_architecture'
        managed = False
        db_table = 'client'

    def __str__(self):
	    return str(self.id) + ': ' + self.name
