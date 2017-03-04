from django.shortcuts import render
from django.contrib import messages
from instaLooter import InstaLooter
import tweepy

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
                alltweets = []

                # make initial request for most recent tweets (200 is the maximum allowed count)
                new_tweets = api.user_timeline(screen_name=screen_name, count=200)

                # save most recent tweets
                alltweets.extend(new_tweets)

                # save the id of the oldest tweet less one
                oldest = alltweets[-1].id - 1

                # keep grabbing tweets until there are no tweets left to grab
                while len(new_tweets) > 0:
                    print "getting tweets before %s" % (oldest)

                    # all subsiquent requests use the max_id param to prevent duplicates
                    new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)

                    # save most recent tweets
                    alltweets.extend(new_tweets)

                    # update the id of the oldest tweet less one
                    oldest = alltweets[-1].id - 1

                    #print "...%s tweets downloaded so far" % (len(alltweets))

                # transform the tweepy tweets into a 2D array that will populate the csv
                outtweets = [[tweet.text.encode("utf-8")] for tweet in alltweets]
                print(outtweets)

                pass

            get_all_tweets(username)

    else:
        form = NameForm()

    return render(request, 'twitter.html', {'form': form})


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


    if request.method == "POST":
        form = UploadPhotoForm(data=request.POST, files=request.FILES, )
        if form.is_valid():
            form.save()
            # api call to server Vova
            photo = Photo.objects.last()
            print photo.preview.url

            messages.success(request, u"Success")
        else:
            form = UploadPhotoForm()

    form = UploadPhotoForm()

    return render(request, 'photo.html', {"form": form })
