from django.db import models


# Create your models here.

class Countrie(models.Model):
    id_country = models.IntegerField(primary_key=True, null=False)
    name = models.CharField(max_length=50)
    iso2 = models.CharField(max_length=2)
    iso3 = models.CharField(max_length=3)



    def __str__(self):
        return self.name