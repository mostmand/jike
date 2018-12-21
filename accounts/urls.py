from django.urls import path
from django.views.generic import TemplateView

from accounts import views

urlpatterns = [
    path('signup', views.signup),
    path('signup/register', views.register),
    path('profile', views.profile)
]
