from django.db import models


# Create your models here.

class Unity(models.Model):
    id_unity = models.IntegerField(primary_key=True,null=False)
    name = models.CharField(max_length=10)


    def __str__(self):
        return self.name