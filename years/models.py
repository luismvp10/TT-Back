from django.db import models




# Create your models here.

class Year(models.Model):
    id_year = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45)



    def __str__(self):
        return self.name
