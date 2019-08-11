from django.db import models
from chapters.models import Chapter
from shipments.models import Shipment
from subshipments.models import Subshipment
from units.models import Unity


# Create your models here.

class Section(models.Model):
    id_section = models.CharField(max_length=8, primary_key=True, null=False, blank=False)
    name = models.CharField(max_length=250)
    subShipment = models.ForeignKey(Subshipment, null=False, blank=False, on_delete=models.CASCADE)
    # id_shipment = models.ForeignKey(Shipment, db_column='id_shipment', null=False, on_delete=models.CASCADE)
    # id_chapter = models.ForeignKey(Chapter, db_column='id_chapter', null=False, on_delete=models.CASCADE)
    id_unity = models.ForeignKey(Unity, db_column='id_unity', null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.name