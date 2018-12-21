from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render

from accounts.models import ExtendedUser


def register(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')
    user = User.objects.create_user(username, email, password)
    user.save()
    extended_user = ExtendedUser.objects.create(user=user, first_name=first_name, last_name=last_name)
    user.save()
    extended_user.save()

    return HttpResponseRedirect('/accounts/login')


def index(request):
    return render(request, 'signup.html')
