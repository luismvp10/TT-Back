from django.db import models
from chapters.models import Chapter




# Create your models here.

class Shipment(models.Model):
    id_shipment= models.CharField(max_length=4, primary_key=True)
    name = models.CharField(max_length=250)
    id_chapter =models.ForeignKey(Chapter, db_column='id_chapter', null=False, on_delete=models.CASCADE)



    def __str__(self):
        return self.name