from django.db import models



# Create your models here.

class Kind(models.Model):
    id_kind = models.CharField(max_length=1, primary_key=True, null=False)
    name = models.CharField(max_length=45)


    def __str__(self):
        return self.name