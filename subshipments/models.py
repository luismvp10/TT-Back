from django.db import models
from chapters.models import Chapter
from shipments.models import Shipment


# Create your models here.

class Subshipment(models.Model):
    id_subShipment = models.CharField(max_length=6, primary_key=True)
    name = models.CharField(max_length=250)
    id_shipment = models.ForeignKey(Shipment, db_column='id_shipment', null=False, on_delete=models.CASCADE)
    id_chapter = models.ForeignKey(Chapter, db_column='id_chapter', null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

