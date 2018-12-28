from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.db import models


class ExtendedUser(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    avatar = models.ImageField(upload_to='accounts/images', null=True)


class UsersIP(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    ip = models.CharField(max_length=15)
    session_id = models.CharField(max_length=20, null=True)
