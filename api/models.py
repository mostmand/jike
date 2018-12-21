from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class SessionV1(models.Model):
    auth_key = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('date published')


class SessionV2(models.Model):
    auth_key = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('date published')