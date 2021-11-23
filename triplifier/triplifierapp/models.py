from django.db import models

# Create your models here.

class csvModel(models.Model):
    csvFileName = models.CharField(max_length=50)
    csvFile = models.FileField(upload_to='tpData/csv/')

    def __str__(self):
        return self.csvFileName

class ttlModel(models.Model):
    ttlFileName = models.CharField(max_length=50)
    ttlFile = models.FileField()

    def __str__(self):
        return self.ttlFileName