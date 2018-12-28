import uuid

from django.contrib.auth.models import User


# Create your views here.
from django.http import HttpResponseBadRequest, HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from api.models import SessionV1, SessionV2, failed_try
from ids.views import log_ddos, get_client_ip
from twitter.models import Tweet


@csrf_exempt
def v1_login(request):
    log_ddos(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.get(username=username)
        if user is not None and user.check_password(password):
            result = str(uuid.uuid4())
            SessionV1.objects.filter(user_id=user.id).delete()
            session = SessionV1.objects.create(user_id=user.id, auth_key=result, pub_date=timezone.now())
            session.save()
            return HttpResponse(result)
        else:
            current_ip = get_client_ip(request)
            row = failed_try.objects.create(ip=current_ip, pub_date=timezone.now())
            row.save()

            if failed_try.objects.filter(ip=current_ip).count() > 5:
                return HttpResponse('Request Blocked')

    return HttpResponseBadRequest()


@csrf_exempt
def v1_tweet(request):
    log_ddos(request)
    if request.method == 'POST':
        auth_key = request.POST['auth_key']
        tweet_title = request.POST['tweet_title']
        tweet_text = request.POST['tweet_text']
        try:
            session = SessionV1.objects.get(auth_key=auth_key)
        except SessionV1.DoesNotExist:
            return HttpResponseBadRequest()
        else:
            user_id = session.user_id
            tweet = Tweet.objects.create(user_id=user_id, tweet_text=tweet_text,
                                         pub_date=timezone.now(), title=tweet_title)
            tweet.save()
            return HttpResponse('/twitter/' + str(tweet.id))

    return HttpResponseBadRequest()


@csrf_exempt
def v2_tweet(request):
    log_ddos(request)
    if request.method == 'POST':
        auth_key = request.POST['auth_key']
        tweet_title = request.POST['tweet_title']
        tweet_text = request.POST['tweet_text']
        try:
            session = SessionV2.objects.get(auth_key=auth_key)
        except SessionV2.DoesNotExist:
            return HttpResponseBadRequest()
        else:
            user_id = session.user_id
            tweet = Tweet.objects.create(user_id=user_id, tweet_text=tweet_text,
                                         pub_date=timezone.now(), title=tweet_title)
            tweet.save()
            return HttpResponse('/twitter/' + str(tweet.id))

    return HttpResponseBadRequest()
