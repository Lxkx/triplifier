from django.db import models
import pandas as pd

# Create your models here.

class csvModel(models.Model):
    csvFileName = models.CharField(max_length=50)
    csvFile = models.FileField(upload_to='tpData/csv/')

    def __str__(self):
        return self.csvFileName

    def content(self):
    	text=self.csvFile.open().read()
    	text=text.decode("utf-8") 
    	text = text.replace('\n','<br>')
    	return text

class ttlModel(models.Model):
    ttlFileName = models.CharField(max_length=50)
    ttlFile = models.FileField()

    def __str__(self):
        return self.ttlFileName

    def content(self):
    	text=open("tpData/ttl/"+self.ttlFileName+".ttl", "r").read()
    	text = text.replace('\n','<br>')
    	text = text.replace('p:','&emsp;&emsp;&emsp;p:')
    	text = text.replace('@prefix &emsp;&emsp;&emsp;p:','@prefix :p')
    	return text