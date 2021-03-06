import uuid

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.template import loader
from django.urls import reverse
from django.utils import timezone

from api.models import SessionV2
from ids.views import log_ddos
from twitter.models import Tweet


def index(request):
    log_ddos(request)
    latest_tweets = Tweet.objects.order_by('-pub_date')[:10]

    template = loader.get_template('twitter/index.html')
    context = {
        'latest_question_list': latest_tweets,
    }
    return HttpResponse(template.render(context, request))


def detail(request, tweet_id):
    log_ddos(request)
    tweet = get_object_or_404(Tweet, pk=tweet_id)
    return render(request, 'twitter/detail.html', {'tweet': tweet})


def create(request):
    log_ddos(request)
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/account/login')

    template = loader.get_template('twitter/create.html')
    return HttpResponse(template.render(request=request))


# return render(request, 'twitter/create.html')


def submit(request):
    log_ddos(request)
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/account/login')

    if request.method == 'POST':
        tweet_title = request.POST['title']
        tweet_text = request.POST['tweet_text']
        tweet = Tweet.objects.create(title=tweet_title, tweet_text=tweet_text, pub_date=timezone.now(), user_id=request.user.id)
        tweet.save()
        return HttpResponseRedirect(reverse('twitter:index', args=()))
    else:
        return HttpResponseBadRequest()


def api_key(request):
    log_ddos(request)
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/account/login')

    result = str(uuid.uuid4())
    SessionV2.objects.filter(user_id=request.user.id).delete()
    session = SessionV2.objects.create(user_id=request.user.id, auth_key=result, pub_date=timezone.now())
    session.save()
    return HttpResponse(result)
