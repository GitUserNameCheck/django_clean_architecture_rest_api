from django.db import models
from clean_architecture.modules.infrastructure.db import Employee, Service
from django_mongodb_backend.fields import EmbeddedModelField, ArrayField
from django_mongodb_backend.models import EmbeddedModel

class Service(EmbeddedModel):
    id = models.IntegerField(default=0)
    price = models.BigIntegerField(blank=True, null=True, validators=[])
    description = models.CharField(max_length=1000, db_collation='Cyrillic_General_CI_AS', blank=True, null=True)

    def __str__(self):
        return str(self.id)

class Employee(EmbeddedModel):
    id = models.IntegerField(default=0)
    name = models.CharField(max_length=500, db_collation='Cyrillic_General_CI_AS', blank=True, null=True)

    def __str__(self):
         return str(self.id)

class ServiceEmployee(models.Model):
    employee = EmbeddedModelField(Employee)
    service = EmbeddedModelField(Service)

    class Meta:
        app_label = 'clean_architecture'
        managed = False
        db_table = 'service_employee'

    def __str__(self):
	    return str(self.id) + ': ' + str(self.employee.name) + "; " + str(self.service.description)