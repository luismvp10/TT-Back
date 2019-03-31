from django.db import models

class Transaction(models.Model):
    id = models.IntegerField(primary_key=True)
    price = models.FloatField()
    weight = models.FloatField()
