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
    kind = models.ForeignKey(Kind, null=False, blank=False, on_delete=models.CASCADE)
    country = models.ForeignKey(Countrie, null=False, blank=False, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, db_column='id_section', null=False, blank=False, on_delete=models.CASCADE)
    year = models.ForeignKey(Year, null=False, db_column='id_year', blank=False, on_delete=models.CASCADE)
    month = models.ForeignKey(Month, null=False, db_column='id_month', blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id_transaction)
