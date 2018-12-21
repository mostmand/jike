from django.urls import path
from django.views.generic import TemplateView

from accounts import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
]
