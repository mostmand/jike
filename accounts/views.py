import uuid

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse
from django.shortcuts import render
from django.utils import timezone

from accounts.forms import UploadPhotoForm
from accounts.models import ExtendedUser
from api.models import SessionV2
from ids.views import log_ddos


def register(request):
    log_ddos(request)
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


def signup(request):
    log_ddos(request)
    return render(request, 'signup.html')


def profile(request):
    log_ddos(request)
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/accounts/login')
    else:
        user_info = ExtendedUser.objects.filter(user_id=request.user.id)
        context = {}
        photo_path = '/static/accounts/content/images/profile-placeholder.jpg'
        if user_info.exists():
            user_info = user_info.first()
            context = {
                "first_name": user_info.first_name,
                "last_name": user_info.last_name,
            }
            if user_info.avatar:
                photo_path = user_info.avatar.url

        context["photo_path"] = photo_path

        return render(request, 'profile.html', context)


def upload_photo(request):
    log_ddos(request)
    if request.method == 'POST':
        form = UploadPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            user = ExtendedUser.objects.filter(user_id=request.user.id)
            if user.exists():
                user = user.first()
                user.avatar = request.FILES['photo']
            else:
                user = ExtendedUser.objects.create(avatar=request.FILES['photo'], user=request.user)
            user.save()
    else:
        form = UploadPhotoForm()
    return HttpResponseRedirect('/account/profile')


def get_authentication_key(request):
    log_ddos(request)
    result = str(uuid.uuid4())
    SessionV2.objects.filter(user_id=request.user.id).delete()
    session = SessionV2.objects.create(user_id=request.user.id, auth_key=result, pub_date=timezone.now())
    session.save()
    return HttpResponse(result)
