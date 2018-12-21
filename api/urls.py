from django.urls import path

from . import views

app_name = 'api'
urlpatterns = [
    # ex: /v1/login
    path('v1/login', views.v1_login, name='v1_login'),
    # ex: /v1/tweet
    path('v1/tweet', views.v1_tweet, name='v1_tweet'),
    # ex: /v2/tweet
    path('v2/tweet', views.v2_tweet, name='v2_tweet'),
]