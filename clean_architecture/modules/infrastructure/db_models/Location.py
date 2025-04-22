from django.db import models

class Location(models.Model):
    id = models.BigAutoField(primary_key=True)
    address = models.CharField(max_length=500, db_collation='Cyrillic_General_CI_AS', blank=True, null=True)

    class Meta:
        app_label = 'clean_architecture'
        managed = False
        db_table = 'location'

    def __str__(self):
	    return str(self.id) + ': ' + self.address