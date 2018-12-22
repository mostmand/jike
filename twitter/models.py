from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from jike import settings


class Tweet(models.Model):
    title = models.CharField(max_length=100, null=False, default='new tweet')
    tweet_text = models.CharField(max_length=300, null=False, default='tweet text')
    pub_date = models.DateTimeField('date published', null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
