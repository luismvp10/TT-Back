from django.db import models
from chapters.models import Chapter




# Create your models here.

class Shipment(models.Model):
    id_shipment = models.CharField(max_length=4, primary_key=True, null=False)
    name = models.CharField(max_length=250)
    chapter = models.ForeignKey(Chapter,  null=False, blank=False, on_delete=models.CASCADE)



    def __str__(self):
        return self.name