from django.db import models
from django_mongodb_backend.fields import ArrayField
from django_mongodb_backend.fields import ObjectIdField

class Client(models.Model):
    _id = ObjectIdField(primary_key=True)
    # _id = models.CharField(max_length=24, primary_key=True)
    name = models.CharField(max_length=500, db_collation='Cyrillic_General_CI_AS', blank=True, null=True)
    events = ArrayField(models.CharField(max_length=24), null=True, blank=True)

    class Meta:
        app_label = 'clean_architecture'
        managed = False
        db_table = 'client'

    def __str__(self):
	    return str(self._id) + ': ' + self.name
