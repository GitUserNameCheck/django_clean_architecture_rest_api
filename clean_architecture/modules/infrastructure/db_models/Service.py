from django.db import models

class Service(models.Model):
    id = models.BigAutoField(primary_key=True)
    price = models.BigIntegerField(blank=True, null=True, validators=[])
    description = models.CharField(max_length=1000, db_collation='Cyrillic_General_CI_AS', blank=True, null=True)

    class Meta:
        app_label = 'clean_architecture'
        managed = False
        db_table = 'service'

    def get_display_price(self):
        return self.price / 100

    def __str__(self):
	    return str(self.id) + ': ' + str(self.get_display_price()) +"; " + self.description