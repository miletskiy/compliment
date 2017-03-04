from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from instaLooter import InstaLooter

from .forms import (
    NameForm,
    UploadPhotoForm,
)


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
                for media in looter.medias():
                    if media['is_video']:
                        url = looter.get_post_info(media['code'])['video_url']
                    else:
                        url = media['display_src']
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

            fcd = form.cleaned_data
            photo = fcd.get("preview")
            print photo

            form.save()

            messages.success(request, u"Success")
        else:
            form = UploadPhotoForm()

    form = UploadPhotoForm()

    return render(request, 'photo.html', {"form": form })
