from django.urls import path
from django.views.generic import TemplateView

from accounts import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='signup.html')),
    path('register', views.register),
]
