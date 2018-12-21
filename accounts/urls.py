from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from accounts import views
from jike import settings

urlpatterns = [
    path('signup', views.signup),
    path('signup/register', views.register),
    path('profile', views.profile),
    path('profile/upload_photo', views.upload_photo)
] + staticfiles_urlpatterns() + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
