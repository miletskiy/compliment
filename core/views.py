from django.shortcuts import render


def index(request):
    """
    Main view
    """

    return render(request, 'core.html')
