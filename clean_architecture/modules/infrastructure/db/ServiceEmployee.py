from django.db import models
from django_mongodb_backend.fields import EmbeddedModelField, ArrayField
from django_mongodb_backend.models import EmbeddedModel
from clean_architecture.modules.infrastructure.db import Employee, Service

class ServiceEmployee(models.Model):
    employee = EmbeddedModelField(Employee)
    service = EmbeddedModelField(Service)

    class Meta:
        app_label = 'clean_architecture'
        managed = False
        db_table = 'service_employee'

    def __str__(self):
	    return str(self.id) + ': ' + str(self.employee.name) + "; " + str(self.service.description)