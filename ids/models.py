from django.db import models


# Create your models here.
class ddos(models.Model):
    browser = models.CharField(max_length=100)
    ip = models.CharField(max_length=15)
    pub_date = models.DateTimeField('date published')


class bruteForce(models.Model):
    browser = models.CharField(max_length=100)
    ip = models.CharField(max_length=15)
    pub_date = models.DateTimeField('date published')
