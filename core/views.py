from django.shortcuts import render
from django.contrib import messages
from instaLooter import InstaLooter

import re
import tweepy
import requests

VISION_SERVER = "http://138.68.78.155:8080"
DJANGO_SERVER = "http://138.68.78.155:8000"

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
    text="success"
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

                # initialize a list to hold all the tweepy Tweets
                all_tweets = []

                # make initial request for most recent tweets (200 is the maximum allowed count)
                new_tweets = api.user_timeline(screen_name=screen_name, count=200)

                # save most recent tweets
                all_tweets.extend(new_tweets)

                # save the id of the oldest tweet less one
                oldest = all_tweets[-1].id - 1

                # keep grabbing tweets until there are no tweets left to grab
                while len(new_tweets) > 0:
                    print "getting tweets before %s" % (oldest)

                    # all subsiquent requests use the max_id param to prevent duplicates
                    new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)

                    # save most recent tweets
                    all_tweets.extend(new_tweets)

                    # update the id of the oldest tweet less one
                    oldest = all_tweets[-1].id - 1

                    #print "...%s tweets downloaded so far" % (len(all_tweets))

                # transform the tweepy tweets into a 2D array that will populate the csv

                processed_tweets = []
                for tweet in all_tweets:
                    processed_tweets.append(' '.join(re.sub(
                        "(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet.text
                        ).split()))

                text_request = "*".join(processed_tweets)

                params = {
                    "url": text_request
                }

                response = requests.get(VISION_SERVER,params)

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
    Instagram view
    """
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)

        if form.is_valid():
            username=form.cleaned_data.get("user_name")
            looter=InstaLooter(profile=username)
            with open("outimagesfile.txt", "w") as output:
                IMG_QUANTITY = 0
                for media in looter.medias():
                    if media['is_video']:
                        url = looter.get_post_info(media['code'])['video_url']
                    else:
                        url = media['display_src']
                    IMG_QUANTITY+=1
                    if IMG_QUANTITY==10:
                        break
                    output.write("{}\n".format(url))

            with open("outcomments.txt", "w") as output:
                for media in looter.medias():
                    post_info = looter.get_post_info(media['code'])
                    for comment in post_info['comments']['nodes']:
                        comm = comment['text']
                    output.write("{}\n".format(comm))
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            #return HttpResponseRedirect('/thanks/')

    else:
        form = NameForm()

    return render(request, 'instagram.html', {'form': form})


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
            print url
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
