import uuid

from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.utils import timezone
from accounts.forms import UploadPhotoForm, CaptchaForm
from accounts.models import ExtendedUser, FailedLoginAttempts
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
        return HttpResponseRedirect('/account/login')
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


def send_email(user_email):
    pass


def login_view(request):
    log_ddos(request)
    if request.method == 'POST':
        captcha_required = False
        failed_attempts: QuerySet = FailedLoginAttempts.objects.filter(ip=get_client_ip(request))
        if failed_attempts.exists():
            if failed_attempts.count() > 15:
                captcha_required = True

        if captcha_required:
            form = CaptchaForm(request.POST)
            if not form.is_valid():
                return HttpResponseRedirect('/account/login')

        username = request.POST['username']
        password = request.POST['password']
        user_attempt = authenticate(request, username=username, password=password)
        if user_attempt is not None:
            login(request, user_attempt)
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/account/login')
    else:
        captcha_required = False
        failed_attempts: QuerySet = FailedLoginAttempts.objects.filter(ip=get_client_ip(request))
        if failed_attempts.exists():
            if failed_attempts.count() > 15:
                captcha_required = True
            pass_mismatch_failed_attempts = failed_attempts.filter(user__isnull=False)
            if pass_mismatch_failed_attempts.count() > 15:
                user_email = pass_mismatch_failed_attempts.first().user.email
                send_email(user_email)
        if captcha_required:
            form = CaptchaForm()
            return render(request, 'registration/login.html', {'form': form})
        else:
            return render(request, 'registration/login.html')


def logout_view(request):
    log_ddos(request)
    logout(request)
    return HttpResponseRedirect('/')


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
