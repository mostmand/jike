from django.contrib import admin

# Register your models here.
from twitter.models import Tweet

admin.site.register(Tweet)
