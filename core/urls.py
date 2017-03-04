
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]

# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)