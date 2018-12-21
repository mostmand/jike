from django.contrib.auth.models import User
from django.db import models


class ExtendedUser(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

