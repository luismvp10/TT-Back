from django.db import models




# Create your models here.

class Chapter(models.Model):
    id_chapter = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=250)



    def __str__(self):
        return self.name