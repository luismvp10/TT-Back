from django.db import models
from chapters.models import Chapter
from shipments.models import Shipment


# Create your models here.

class Subshipment(models.Model):
    id_subShipment = models.CharField(max_length=6, primary_key=True, null=False)
    name = models.CharField(max_length=250)
    shipment = models.ForeignKey(Shipment, blank=False, db_column='id_shipment', null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

