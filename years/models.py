from django.db import models
from months.models import Month

# Create your models here.

class Year(models.Model):
    id_year = models.IntegerField(primary_key=True, null=False)
    name = models.CharField(max_length=45)


    def __str__(self):
        return self.name










# class Year_has_month(models.Model):
#     id_year = models.ForeignKey(Year, db_column='id_year', null=False, on_delete=models.CASCADE)
#     id_month = models.ForeignKey(Month, db_column='id_month', null=False, on_delete=models.CASCADE)

