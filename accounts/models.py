from django.contrib.auth import user_logged_in, user_logged_out, user_login_failed
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.db import models
from django.dispatch import receiver


class ExtendedUser(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    avatar = models.ImageField(upload_to='accounts/images', null=True)


class UsersIP(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    ip = models.CharField(max_length=15)
    session_id = models.CharField(max_length=20, null=True)


class FailedLoginAttempts(models.Model):
    ip = models.CharField(max_length=15, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    login_attempts_query = FailedLoginAttempts.objects.filter(ip=get_client_ip(request))
    if login_attempts_query.exists():
        login_attempts_query.delete()


@receiver(user_login_failed)
def user_login_failed_callback(sender, credentials, request, **kwargs):
    user_query = User.objects.filter(username=credentials['username'])
    ip = get_client_ip(request)
    failed = FailedLoginAttempts.objects.create(ip=ip)
    if user_query.exists():
        user = user_query.first()
        failed.user = user

    failed.save()


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
