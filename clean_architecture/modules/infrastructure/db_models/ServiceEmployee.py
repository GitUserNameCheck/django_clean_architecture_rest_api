from django.db import models
from django_mongodb_backend.fields import EmbeddedModelField, ArrayField
from django_mongodb_backend.models import EmbeddedModel
from django_mongodb_backend.fields import ObjectIdField
from clean_architecture.modules.infrastructure.db_models import Employee, Service

class ServiceEmployee(models.Model):
    _id = ObjectIdField(primary_key=True)
    employee = EmbeddedModelField(Employee)
    service = EmbeddedModelField(Service)

    class Meta:
        app_label = 'clean_architecture'
        managed = False
        db_table = 'service_employee'

    def __str__(self):
	    return str(self.id) + ': ' + str(self.employee.name) + "; " + str(self.service.description)