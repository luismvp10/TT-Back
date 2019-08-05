from django.db import models
from kinds.models import Kind
from countries.models import Countrie
from sections.models import Section
from subshipments.models import Subshipment
from chapters.models import Chapter
from years.models import Year
from months.models import Month

class Transaction(models.Model):
    id_transaction = models.IntegerField(primary_key=True, null=False)
    price = models.FloatField()
    weight = models.FloatField()
    id_kind = models.ForeignKey(Kind, db_column='id_kind', null=False, on_delete=models.CASCADE)
    id_country = models.ForeignKey(Countrie, db_column='id_country', null=False, on_delete=models.CASCADE)
    id_section = models.ForeignKey(Section, db_column='id_section', null=False, on_delete=models.CASCADE)
    id_subShipment = models.ForeignKey(Subshipment, db_column='id_subShipment', null=False, on_delete=models.CASCADE)
    id_chapter = models.ForeignKey(Chapter, db_column='id_chapter', null=False, on_delete=models.CASCADE)
    id_year = models.ForeignKey(Year, db_column='id_year', null=False, on_delete=models.CASCADE)
    id_month = models.ForeignKey(Month, db_column='id_month', null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.name