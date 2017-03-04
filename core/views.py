from django.shortcuts import render
from django.contrib import messages
from instaLooter import InstaLooter
import requests

VOVA_SERVER = "http://138.68.78.155:8080"
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

    return render(request, 'twitter.html')


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
    text = u"Success"

    if request.method == "POST":
        form = UploadPhotoForm(data=request.POST, files=request.FILES, )
        if form.is_valid():
            form.save()
            # api call to server Vova
            photo = Photo.objects.last()
            # TODO: need refactor to use get_current_host()
            url = "{server}{url}".format(**{"server": DJANGO_SERVER, "url": photo.preview.url, })
            print url
            url = "{server}{url}".format(**{"server": DJANGO_SERVER, "url": "/media/photos/2017/03/04/compliment.jpg", })
            params = {"url": url}
            response = requests.get(url=VOVA_SERVER, params=params, )

            text = response.text if response.ok else u"Something went wrong ({error})".format(**{"error": response.status_code})

            messages.success(request, u"Success")
        else:
            form = UploadPhotoForm()

            messages.success(request, u"Something went wrong ({error})".format(**{"error": form.errors}))

    form = UploadPhotoForm()

    return render(request, 'photo.html', {"form": form, "text": text, })
