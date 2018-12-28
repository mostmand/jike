from django.urls import path
from accounts import views

urlpatterns = [
    path('signup', views.signup),
    path('signup/register', views.register),
    path('profile', views.profile),
    path('profile/upload_photo', views.upload_photo),
    path('get_token', views.get_authentication_key),
    path('login', views.login_view),
    path('logout', views.logout_view)
]
