from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render

from accounts.forms import UploadPhotoForm
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


def signup(request):
    return render(request, 'signup.html')


def profile(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login')
    else:
        user_info = ExtendedUser.objects.get(user_id=request.user.id)
        photo_path = request.user.id


def upload_photo(request):
    if request.method == 'POST':
        form = UploadPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect(request.path_info)
    else:
        form = UploadPhotoForm()
    return render(request, 'upload.html', {'form': form})


def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

