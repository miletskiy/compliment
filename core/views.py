from django.shortcuts import render
from django.contrib import messages
from instaLooter import InstaLooter

import re
import tweepy
import requests
import json

INFO_SERVER = "http://138.68.78.155:8081"
VISION_SERVER = "http://138.68.78.155:8080"
DJANGO_SERVER = "http://138.68.78.155:80"

from .forms import (
    NameForm,
    UploadPhotoForm,
)
from .models import Photo


def index(request):
    """
    Main view
    """


    return render(request, 'core.html')


def twitter(request):
    """
    Twitter view
    """
    text=""
    consumer_key = "7vcleOTNnGiZWSBQVAfcDsYup"
    consumer_secret = "sc6y1yrOO7xNbDTt5HNwvTGwL59cdRDVuf1DOW9yetwrxlhwTH"
    access_key = "838041296296103936-SH8vBxIYv3SfeFqEfhT5OKgSbIajjpB"
    access_secret = "UzOnwUVJRoh8YH2tVnaaF3o5EMdzaLzHRc0nrbQoYG8rM"

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("user_name")
            def get_all_tweets(screen_name):
                # Twitter only allows access to a users most recent 3240 tweets with this method

                # authorize twitter, initialize tweepy
                auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
                auth.set_access_token(access_key, access_secret)
                api = tweepy.API(auth)

                # make initial request for most recent tweets (200 is the maximum allowed count)
                all_tweets = api.user_timeline(screen_name=screen_name, count=10)

                processed_tweets = []
                for tweet in all_tweets:
                    processed_tweets.append(' '.join(re.sub(
                        "(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet.text
                        ).split()))

                params = {
                    "tweets": processed_tweets
                }


                response = requests.post(VISION_SERVER, json.dumps(params), headers={'content-type': 'application/json'})

                if response.ok:
                    text = response.text
                    print(text)
                    return text
                else:
                    text = "error"

            text = get_all_tweets(username)

    else:
        form = NameForm()

    return render(request, 'twitter.html', {'form': form,"text":text})


def instagram(request):
    """
    Twitter view
    """
    text=""
    consumer_key = "7vcleOTNnGiZWSBQVAfcDsYup"
    consumer_secret = "sc6y1yrOO7xNbDTt5HNwvTGwL59cdRDVuf1DOW9yetwrxlhwTH"
    access_key = "838041296296103936-SH8vBxIYv3SfeFqEfhT5OKgSbIajjpB"
    access_secret = "UzOnwUVJRoh8YH2tVnaaF3o5EMdzaLzHRc0nrbQoYG8rM"

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("user_name")
            def get_all_tweets(screen_name):
                # Twitter only allows access to a users most recent 3240 tweets with this method

                # authorize twitter, initialize tweepy
                auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
                auth.set_access_token(access_key, access_secret)
                api = tweepy.API(auth)

                # make initial request for most recent tweets (200 is the maximum allowed count)
                all_tweets = api.user_timeline(screen_name=screen_name, count=200)

                processed_tweets = []
                for tweet in all_tweets:
                    processed_tweets.append(' '.join(re.sub(
                        "(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet.text
                        ).split()))

                params = {
                    "tweets": processed_tweets
                }


                response = requests.post(INFO_SERVER, json.dumps(params), headers={'content-type': 'application/json'})

                if response.ok:
                    text = response.text
                    print(text)
                    return text
                else:
                    text = "error"

            text = get_all_tweets(username)

    else:
        form = NameForm()

    return render(request, 'instagram.html', {'form': form,"text":text})


def photo(request):
    """
    Photo view
    """
    text = ""
    image = None

    if request.method == "POST":
        form = UploadPhotoForm(data=request.POST, files=request.FILES, )
        if form.is_valid():
            form.save()
            image = Photo.objects.last()
            url = DJANGO_SERVER + image.preview.url
            params = { "url" : url }
            response = requests.get(url=VISION_SERVER, params=params, )
            if response.ok:
                text = response.text
                messages.success(request, u"Success")
            else:
                text = u"Something went wrong ({error})".format(**{"error": response.status_code})
                messages.error(request, u"Something went wrong")
        else:
            messages.error(request, u"{error}".format(**{"error": form.errors}))

    form = UploadPhotoForm()

    return render(request, 'photo.html', {"form": form, "text": text, "image": image, })
