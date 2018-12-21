from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.template import loader

from twitter.models import Tweet


def index(request):
    latest_question_list = Tweet.objects.order_by('-pub_date')[:5]
    template = loader.get_template('twitter/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))


def detail(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id)
    return render(request, 'twitter/detail.html', {'tweet': tweet})