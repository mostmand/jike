from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from jike import settings


class Tweet(models.Model):
    tweet_text = models.CharField(max_length=300)
    pub_date = models.DateTimeField('date published')
    user = models.ForeignKey(User, on_delete=models.CASCADE)