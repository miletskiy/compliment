from django.shortcuts import render



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

    return render(request, 'instagram.html')


def photo(request):
    """
    Photo view
    """

    return render(request, 'photo.html')
