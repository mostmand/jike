from django.urls import path

from . import views

app_name = 'twitter'
urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    # ex: /polls/5/
    path('<int:tweet_id>/', views.detail, name='detail'),
    # ex: /create
    path('create', views.create, name='create'),
    path('submit', views.submit, name='submit'),
]