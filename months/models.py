from django.db import models




# Create your models here.

class Month(models.Model):
    id_month = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)



    def __str__(self):
        return self.name
